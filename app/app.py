from flask import (
    Flask,
    render_template,
    request,
    send_file,
    url_for,
    send_from_directory,
    redirect,
    jsonify,
)

import os
import sys
import json
import tempfile
import traceback
import uuid
import threading
from datetime import datetime

# Ensure app directory is on path for modules
BASE_DIR = os.path.dirname(
    os.path.abspath(__file__)
)

if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

import numpy as np

from PIL import Image
from werkzeug.utils import secure_filename

from pdf_generator import generate_pdf

from history import (
    add_prediction,
    get_history,
    clear_history,
    delete_prediction,
)


# ==========================================
# Flask Application
# ==========================================

app = Flask(__name__)

app.secret_key = os.environ.get(
    "SECRET_KEY",
    "smart-agri-advisor-dev-key-change-in-production"
)

app.config.update(
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE="Lax",
)


# ==========================================
# Security Headers
# ==========================================

@app.after_request
def add_security_headers(response):
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "SAMEORIGIN"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    return response


# ==========================================
# Store Latest Prediction
# ==========================================

latest_prediction = {}


# ==========================================
# Base Directory
# ==========================================

BASE_DIR = os.path.dirname(
    os.path.abspath(__file__)
)


# ==========================================
# Upload Configuration
# ==========================================

UPLOAD_FOLDER = os.path.join(
    BASE_DIR,
    "static",
    "uploads"
)


ALLOWED_EXTENSIONS = {
    "png",
    "jpg",
    "jpeg"
}


app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["MAX_CONTENT_LENGTH"] = 16 * 1024 * 1024


os.makedirs(
    UPLOAD_FOLDER,
    exist_ok=True
)


# ==========================================
# Helper Functions
# ==========================================

def allowed_file(filename):

    return (
        "." in filename
        and
        filename.rsplit(
            ".",
            1
        )[1].lower()
        in ALLOWED_EXTENSIONS
    )


def normalize_key(value):

    if not isinstance(value, str):
        return ""

    return (
        value
        .strip()
        .lower()
        .replace(" ", "_")
    )


# ==========================================
# Uploaded Image Route
# ==========================================

@app.route("/uploads/<filename>")
def uploaded_file(filename):

    return send_from_directory(
        app.config["UPLOAD_FOLDER"],
        filename
    )


# ==========================================
# Optimized TFLite CNN Model & Thread Safety
# ==========================================

TFLITE_PATH = os.path.join(
    BASE_DIR,
    "..",
    "models",
    "plant_disease_cnn.tflite"
)

KERAS_PATH = os.path.join(
    BASE_DIR,
    "..",
    "models",
    "plant_disease_cnn.keras"
)

_interpreter = None
_interpreter_lock = threading.Lock()
_input_index = None
_output_index = None


def get_interpreter():
    """
    Thread-safe lazy loader for the optimized TensorFlow Lite CNN model.
    Loads on-demand using LiteRT / TFLite runtime to keep idle memory < 40 MB RSS
    and peak inference memory ~106 MB RSS.
    """
    global _interpreter, _input_index, _output_index

    if _interpreter is None:
        with _interpreter_lock:
            if _interpreter is None:
                try:
                    os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2"
                    os.environ["TF_ENABLE_ONEDNN_OPTS"] = "0"

                    InterpreterClass = None
                    try:
                        from ai_edge_litert.interpreter import Interpreter
                        InterpreterClass = Interpreter
                    except ImportError:
                        try:
                            from tensorflow.lite.python.interpreter import Interpreter
                            InterpreterClass = Interpreter
                        except ImportError:
                            import tensorflow as tf
                            InterpreterClass = tf.lite.Interpreter

                    if os.path.exists(TFLITE_PATH) and InterpreterClass is not None:
                        interp = InterpreterClass(
                            model_path=TFLITE_PATH,
                            num_threads=2
                        )
                        interp.allocate_tensors()
                        _input_index = interp.get_input_details()[0]["index"]
                        _output_index = interp.get_output_details()[0]["index"]
                        _interpreter = interp
                        print("✅ Optimized TFLite CNN Model Lazy-Loaded Successfully", flush=True)
                    elif os.path.exists(KERAS_PATH):
                        print("⚠️ TFLite model not found, falling back to Keras model...", flush=True)
                        import tensorflow as tf
                        keras_model = tf.keras.models.load_model(KERAS_PATH, compile=False)
                        _interpreter = keras_model
                        print("✅ Keras CNN Model Loaded as Fallback", flush=True)
                    else:
                        print(f"⚠️ Neither TFLite ({TFLITE_PATH}) nor Keras ({KERAS_PATH}) model was found.", flush=True)
                except Exception as model_err:
                    print(f"⚠️ Error lazy-loading prediction model: {model_err}", flush=True)

    return _interpreter


# ==========================================
# Load Disease Database
# ==========================================

DATABASE_PATH = os.path.join(
    BASE_DIR,
    "..",
    "database",
    "disease_database.json"
)


with open(
    DATABASE_PATH,
    "r",
    encoding="utf-8"
) as file:

    disease_database = json.load(file)


print(
    "✅ Disease Database Loaded"
)


print(
    "Database Entries:",
    len(disease_database)
)


# ==========================================
# Class Names
# ==========================================

CLASS_NAMES = [

    "Apple___Apple_scab",
    "Apple___Black_rot",
    "Apple___Cedar_apple_rust",
    "Apple___healthy",

    "Blueberry___healthy",

    "Cherry_(including_sour)___Powdery_mildew",
    "Cherry_(including_sour)___healthy",

    "Corn_(maize)___Cercospora_leaf_spot Gray_leaf_spot",
    "Corn_(maize)___Common_rust_",
    "Corn_(maize)___Northern_Leaf_Blight",
    "Corn_(maize)___healthy",

    "Grape___Black_rot",
    "Grape___Esca_(Black_Measles)",
    "Grape___Leaf_blight_(Isariopsis_Leaf_Spot)",
    "Grape___healthy",

    "Orange___Haunglongbing_(Citrus_greening)",

    "Peach___Bacterial_spot",
    "Peach___healthy",

    "Pepper,_bell___Bacterial_spot",
    "Pepper,_bell___healthy",

    "Potato___Early_blight",
    "Potato___Late_blight",
    "Potato___healthy",

    "Raspberry___healthy",

    "Soybean___healthy",

    "Squash___Powdery_mildew",

    "Strawberry___Leaf_scorch",
    "Strawberry___healthy",

    "Tomato___Bacterial_spot",
    "Tomato___Early_blight",
    "Tomato___Late_blight",
    "Tomato___Leaf_Mold",
    "Tomato___Septoria_leaf_spot",
    "Tomato___Spider_mites Two-spotted_spider_mite",
    "Tomato___Target_Spot",
    "Tomato___Tomato_Yellow_Leaf_Curl_Virus",
    "Tomato___Tomato_mosaic_virus",
    "Tomato___healthy"

]


# ==========================================
# Model Validation (Deferred to get_model)
# ==========================================


# ==========================================
# Health Check Endpoint
# ==========================================

@app.route("/health")
def health():

    return jsonify({
        "status": "healthy"
    }), 200


# ==========================================
# Home
# ==========================================

@app.route("/")
def home():

    return render_template(
        "index.html"
    )


# ==========================================
# About
# ==========================================

@app.route("/about")
def about():

    return render_template(
        "about.html"
    )


# ==========================================
# Guide
# ==========================================

@app.route("/guide")
def guide():

    return render_template(
        "guide.html"
    )


# ==========================================
# Prediction History
# ==========================================

@app.route("/history")
def history_page():

    history = get_history()

    # Show latest predictions at the top
    reversed_history = list(reversed(history)) if history else []

    return render_template(
        "history.html",
        history=reversed_history
    )


# ==========================================
# Clear History
# ==========================================

@app.route(
    "/history/clear",
    methods=["POST"]
)
def clear_prediction_history():

    clear_history()

    return redirect(
        url_for("history_page")
    )


# ==========================================
# Delete Single History Record
# ==========================================

@app.route(
    "/history/delete/<int:prediction_id>",
    methods=["POST"]
)
def delete_history_item(prediction_id):

    delete_prediction(prediction_id)

    return redirect(
        url_for("history_page")
    )


# ==========================================
# Prediction
# ==========================================

@app.route(
    "/predict",
    methods=["POST"]
)
def predict():

    global latest_prediction

    try:
        # ======================================
        # Check Image in Request
        # ======================================

        if "image" not in request.files:

            return render_template(
                "error.html",
                error="Please select a plant leaf image before analyzing."
            ), 400


        file = request.files["image"]


        if not file or not file.filename or file.filename.strip() == "":

            return render_template(
                "error.html",
                error="Please select a plant leaf image before analyzing."
            ), 400


        if not allowed_file(
            file.filename
        ):

            return render_template(
                "error.html",
                error=(
                    "Unsupported file type. "
                    "Please upload a valid JPG, JPEG, or PNG image."
                )
            ), 400


        # ======================================
        # Check Empty / Zero-Byte File
        # ======================================

        file.seek(0, os.SEEK_END)
        file_size = file.tell()
        file.seek(0)

        if file_size == 0:

            return render_template(
                "error.html",
                error="The selected file is empty (0 bytes). Please upload a valid image."
            ), 400


        # ======================================
        # Filename Security & Collision Handling
        # ======================================

        clean_name = secure_filename(
            file.filename
        )

        if not clean_name:
            clean_name = "leaf_image.jpg"

        timestamp_prefix = datetime.now().strftime("%Y%m%d_%H%M%S")
        unique_token = uuid.uuid4().hex[:8]
        filename = f"{timestamp_prefix}_{unique_token}_{clean_name}"


        filepath = os.path.join(
            app.config["UPLOAD_FOLDER"],
            filename
        )


        file.save(
            filepath
        )


        # ======================================
        # URL For Uploaded Image
        # ======================================

        image_path = url_for(
            "uploaded_file",
            filename=filename
        )


        # ======================================
        # Image Integrity Verification
        # ======================================

        try:

            with Image.open(filepath) as test_img:
                test_img.verify()

            with Image.open(filepath) as raw_img:
                img = raw_img.convert("RGB")

        except Exception as img_err:

            if os.path.exists(filepath):
                try:
                    os.remove(filepath)
                except OSError:
                    pass

            print(
                "⚠️ Corrupted or invalid image uploaded:",
                img_err
            )

            return render_template(
                "error.html",
                error=(
                    "The uploaded file is corrupted or not a valid image. "
                    "Please select a valid JPG, JPEG, or PNG image."
                )
            ), 400


        # ======================================
        # Model Availability Check (Lazy Load)
        # ======================================

        model = get_interpreter()

        if model is None:

            print("⚠️ Prediction model is not available.", flush=True)

            return render_template(
                "error.html",
                error="The AI prediction model is currently unavailable. Please try again later."
            ), 503


        # ======================================
        # Image Preprocessing & Prediction
        # ======================================

        try:

            img_resized = img.resize(
                (128, 128)
            )

            img_array = np.array(
                img_resized,
                dtype=np.float32
            )

            img_array /= 255.0

            img_array = np.expand_dims(
                img_array,
                axis=0
            )

            # Thread-safe inference execution
            with _interpreter_lock:
                if hasattr(model, "set_tensor"):
                    # TFLite Interpreter execution
                    model.set_tensor(_input_index, img_array)
                    model.invoke()
                    probabilities = model.get_tensor(_output_index)[0]
                else:
                    # Keras Model callable execution (fallback)
                    predictions = model(
                        img_array,
                        training=False
                    ).numpy()
                    probabilities = predictions[0]

        except Exception as pred_err:

            print(
                "⚠️ Prediction error during inference:",
                pred_err
            )

            return render_template(
                "error.html",
                error="An error occurred while analyzing the image. Please try again with a clear leaf photo."
            ), 500


        # ======================================
        # Validate Output
        # ======================================

        if len(probabilities) != len(
            CLASS_NAMES
        ):

            raise ValueError(
                "CNN output does not contain "
                f"{len(CLASS_NAMES)} classes. "
                f"Model returned "
                f"{len(probabilities)}."
            )


        # ======================================
        # Predicted Class
        # ======================================

        predicted_index = int(
            np.argmax(
                probabilities
            )
        )


        predicted_class = (
            CLASS_NAMES[
                predicted_index
            ]
        )


        confidence = (
            float(
                probabilities[
                    predicted_index
                ]
            )
            * 100
        )


        # ======================================
        # Debug
        # ======================================

        print()
        print("=" * 55)
        print("PREDICTION DEBUG")
        print("=" * 55)

        print(
            "Predicted Index :",
            predicted_index
        )

        print(
            "Predicted Class :",
            predicted_class
        )

        print(
            "Confidence      :",
            f"{confidence:.2f}%"
        )

        print(
            "Exact DB Match  :",
            predicted_class in disease_database
        )

        print("=" * 55)


        # ======================================
        # Top 5 Predictions
        # ======================================

        top5_indices = np.argsort(
            probabilities
        )[-5:][::-1]


        chart_labels = []

        chart_values = []


        for index in top5_indices:

            label = CLASS_NAMES[
                int(index)
            ]


            chart_labels.append(
                label.replace(
                    "_",
                    " "
                )
            )


            chart_values.append(
                round(
                    float(
                        probabilities[
                            index
                        ]
                    ) * 100,
                    2
                )
            )


        # ======================================
        # Chart Data
        # ======================================

        chart_data = {

            "labels":
                chart_labels,

            "values":
                chart_values

        }


        # ======================================
        # Ranking
        # ======================================

        ranking = list(
            zip(
                chart_labels,
                chart_values
            )
        )


        # ======================================
        # Database Matching
        # ======================================

        info = disease_database.get(
            predicted_class
        )


        # ======================================
        # Normalized Matching
        # ======================================

        if info is None:

            normalized_prediction = (
                normalize_key(
                    predicted_class
                )
            )


            print(
                "⚠️ Exact database match failed."
            )


            print(
                "Trying normalized matching..."
            )


            for (
                database_key,
                database_info
            ) in disease_database.items():

                if (
                    normalize_key(
                        database_key
                    )
                    ==
                    normalized_prediction
                ):

                    info = database_info


                    print(
                        "✅ Normalized match found:"
                    )


                    print(
                        predicted_class,
                        "->",
                        database_key
                    )


                    break


        # ======================================
        # Final Fallback
        # ======================================

        if info is None:

            print(
                "❌ Disease information not found:",
                predicted_class
            )


            info = {

                "Crop": "Unknown",

                "Disease":
                    predicted_class,

                "Scientific_Name":
                    "Unknown",

                "Pathogen":
                    "Unknown",

                "Pathogen_Type":
                    "Unknown",

                "Category":
                    "Unknown",

                "Affected_Part":
                    "Unknown",

                "Environment":
                    "Information not available.",

                "Spread":
                    "Information not available.",

                "Description":
                    "Information not available.",

                "Cause": [],

                "Age_Cycle": {

                    "Early": "-",

                    "Moderate": "-",

                    "Severe": "-",

                    "Estimated": "-"

                },

                "Symptoms": [],

                "Treatment": [],

                "Organic_Treatment": [],

                "Recommended_Chemicals": [],

                "Prevention": [],

                "Risk_Level":
                    "Unknown",

                "Severity":
                    "Unknown",

                "Recommended_Actions": []

            }


        # ======================================
        # Disease Debug
        # ======================================

        print(
            "Disease Information:",
            info.get(
                "Disease",
                "Unknown"
            )
        )


        print(
            "Crop:",
            info.get(
                "Crop",
                "Unknown"
            )
        )


        print("=" * 55)
        print()


        # ======================================
        # Store Latest Prediction
        # ======================================

        latest_prediction = {
          "prediction": info.get(
             "Disease",
            predicted_class,
        ),
        "confidence": f"{confidence:.2f}%",
        "info": info,
    "image_path": filepath,
}


        # ======================================
        # Save To History
        # ======================================

        try:

            add_prediction(

                prediction=info.get(
                    "Disease",
                    predicted_class
                ),

                confidence=(
                    f"{confidence:.2f}%"
                ),

                info=info,

                image_path=image_path

            )

            print(
                "✅ Prediction saved to history."
            )

        except Exception as history_error:

            print(
                "⚠️ History save failed:",
                history_error
            )


        # ======================================
        # Render Result
        # ======================================

        return render_template(

            "result.html",

            image_path=image_path,

            prediction=info.get(
                "Disease",
                predicted_class
            ),

            confidence=(
                f"{confidence:.2f}%"
            ),

            crop=info.get(
                "Crop",
                "Unknown"
            ),

            description=info.get(
                "Description",
                "Information not available."
            ),

            symptoms=info.get(
                "Symptoms",
                []
            ),

            treatment=info.get(
                "Treatment",
                []
            ),

            prevention=info.get(
                "Prevention",
                []
            ),

            info=info,

            chart_data=chart_data,

            ranking=ranking

        )


    # ==========================================
    # Error Handling
    # ==========================================

    except Exception as e:

        traceback.print_exc()

        return render_template(
            "error.html",
            error="An unexpected error occurred while processing your diagnosis. Please try again."
        ), 500


# ==========================================
# Download PDF Report
# ==========================================

@app.route(
    "/download_report"
)
def download_report():

    global latest_prediction


    # ======================================
    # Check Prediction
    # ======================================

    if not latest_prediction or not isinstance(latest_prediction, dict):

        return render_template(
            "error.html",
            error=(
                "No prediction available. "
                "Please analyze an image first."
            )
        ), 400


    try:

        # ==================================
        # Temporary PDF
        # ==================================

        with tempfile.NamedTemporaryFile(
            delete=False,
            suffix=".pdf"
        ) as temp_file:

            pdf_path = (
                temp_file.name
            )


        # ==================================
        # Generate PDF
        # ==================================

        generate_pdf(
            output_path=pdf_path,
            info=latest_prediction.get("info", {}),
            prediction=latest_prediction.get("prediction", "Unknown"),
            confidence=latest_prediction.get("confidence", "N/A"),
            image_path=latest_prediction.get("image_path"),
        )


        # ==================================
        # Send PDF
        # ==================================

        return send_file(
            pdf_path,
            as_attachment=True,
            download_name=(
                "Plant_Disease_Report.pdf"
            ),
            mimetype=(
                "application/pdf"
            )
        )


    except Exception as e:

        traceback.print_exc()

        return render_template(
            "error.html",
            error="Unable to generate the PDF report at this time. Please try again."
        ), 500


# ==========================================
# HTTP Error Handlers
# ==========================================

@app.errorhandler(400)
def bad_request(e):

    return render_template(
        "error.html",
        error="Bad Request (400). The server could not understand or process the request."
    ), 400


@app.errorhandler(404)
def page_not_found(e):

    return render_template(
        "error.html",
        error="The requested page could not be found (404)."
    ), 404


@app.errorhandler(405)
def method_not_allowed(e):

    return render_template(
        "error.html",
        error="Method Not Allowed (405). The requested HTTP method is not supported for this page."
    ), 405


@app.errorhandler(413)
def request_entity_too_large(e):

    return render_template(
        "error.html",
        error="The uploaded image file is too large. Please upload an image smaller than 16 MB."
    ), 413


@app.errorhandler(500)
def internal_server_error(e):

    return render_template(
        "error.html",
        error="An internal server error occurred (500). Please try again later."
    ), 500


# ==========================================
# Run Flask Application
# ==========================================

if __name__ == "__main__":

    debug_mode = os.environ.get("FLASK_DEBUG", "1").strip().lower() in (
        "true",
        "1",
        "yes"
    )

    host = os.environ.get("HOST", os.environ.get("FLASK_HOST", "127.0.0.1"))
    port = int(os.environ.get("PORT", os.environ.get("FLASK_PORT", 5000)))

    app.run(
        debug=debug_mode,
        host=host,
        port=port
    )