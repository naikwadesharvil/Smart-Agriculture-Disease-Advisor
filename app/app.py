from flask import (
    Flask,
    render_template,
    request,
    send_file,
    url_for,
    send_from_directory,
)

import os
import json
import tempfile
import traceback

import numpy as np
import tensorflow as tf

from PIL import Image
from werkzeug.utils import secure_filename

from pdf_generator import generate_pdf

from history import add_prediction


# ==========================================
# Flask Application
# ==========================================

app = Flask(__name__)


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
# Load CNN Model
# ==========================================

MODEL_PATH = os.path.join(
    BASE_DIR,
    "..",
    "models",
    "plant_disease_cnn.keras"
)


MODEL = tf.keras.models.load_model(
    MODEL_PATH,
    compile=False
)


MODEL.compile(
    optimizer="adam",
    loss="sparse_categorical_crossentropy",
    metrics=["accuracy"]
)


print(
    "✅ CNN Model Loaded Successfully"
)


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
# Validate Model / Classes
# ==========================================

try:

    model_output_size = MODEL.output_shape[-1]

    if model_output_size != len(CLASS_NAMES):

        raise ValueError(
            f"Model output has {model_output_size} classes "
            f"but CLASS_NAMES contains {len(CLASS_NAMES)}."
        )

except Exception as e:

    print(
        "⚠️ Model/Class validation:",
        str(e)
    )


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
# Prediction
# ==========================================

@app.route(
    "/predict",
    methods=["POST"]
)
def predict():

    global latest_prediction

    try:
        print("\n========== UPLOAD DEBUG ==========")
        print("request.files:", request.files)
        print("request.form:", request.form)
        print(
            "image in request.files:",
            "image" in request.files
        )
        print("==================================\n")

        if "image" not in request.files:

            return render_template(
                "error.html",
                error="No image uploaded."
            )

        # ======================================
        # Check Image
        # ======================================

        if "image" not in request.files:

            return render_template(
                "error.html",
                error="No image uploaded."
            )


        file = request.files["image"]


        if file.filename == "":

            return render_template(
                "error.html",
                error="No file selected."
            )


        if not allowed_file(
            file.filename
        ):

            return render_template(
                "error.html",
                error=(
                    "Unsupported file type. "
                    "Please upload JPG, JPEG or PNG."
                )
            )


        # ======================================
        # Save Image
        # ======================================

        filename = secure_filename(
            file.filename
        )


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
        # Image Preprocessing
        # ======================================

        img = Image.open(
            filepath
        ).convert("RGB")


        img = img.resize(
            (128, 128)
        )


        img_array = np.array(
            img,
            dtype=np.float32
        )


        img_array /= 255.0


        img_array = np.expand_dims(
            img_array,
            axis=0
        )


        # ======================================
        # CNN Prediction
        # ======================================

        predictions = MODEL.predict(
            img_array,
            verbose=0
        )


        probabilities = predictions[0]


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

            error=str(e)

        )


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

    if not latest_prediction:

        return render_template(

            "error.html",

            error=(
                "No prediction available. "
                "Please analyze an image first."
            )

        )


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
          info=latest_prediction["info"],
          prediction=latest_prediction["prediction"],
          confidence=latest_prediction["confidence"],
          image_path=latest_prediction["image_path"],
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

            error=(
                "Failed to generate PDF: "
                + str(e)
            )

        )


# ==========================================
# Run Flask Application
# ==========================================

if __name__ == "__main__":

    app.run(
        debug=True
    )