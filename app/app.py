from flask import (
    Flask,
    render_template,
    request,
    send_file
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

# ==========================================
# Flask Application
# ==========================================

app = Flask(__name__)

# ==========================================
# Store Latest Prediction
# ==========================================

latest_prediction = {}

# ==========================================
# Upload Configuration
# ==========================================

UPLOAD_FOLDER = os.path.join(
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
# Helper Function
# ==========================================

def allowed_file(filename):

    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower()
        in ALLOWED_EXTENSIONS
    )

# ==========================================
# Load CNN Model
# ==========================================

MODEL_PATH = os.path.join(
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

print("✅ CNN Model Loaded Successfully")

# ==========================================
# Load Disease Database
# ==========================================

DATABASE_PATH = os.path.join(
    "..",
    "database",
    "disease_database.json"
)

with open(DATABASE_PATH, "r") as file:

    disease_database = json.load(file)

print("✅ Disease Database Loaded")

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
# Home Route
# ==========================================

@app.route("/")
def home():
    return render_template("index.html")


# ==========================================
# About Route
# ==========================================

@app.route("/about")
def about():
    return render_template("about.html")


# ==========================================
# Guide Route
# ==========================================

@app.route("/guide")
def guide():
    return render_template("guide.html")


# ==========================================
# Prediction Route
# ==========================================

@app.route("/predict", methods=["POST"])
def predict():

    global latest_prediction

    try:

        # ----------------------------------
        # Check Uploaded Image
        # ----------------------------------

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

        if not allowed_file(file.filename):

            return render_template(
                "error.html",
                error="Unsupported file type. Please upload JPG, JPEG or PNG."
            )

        # ----------------------------------
        # Save Uploaded Image
        # ----------------------------------

        filename = secure_filename(file.filename)

        filepath = os.path.join(
            app.config["UPLOAD_FOLDER"],
            filename
        )

        file.save(filepath)

        image_path = filepath.replace("\\", "/")

        # ----------------------------------
        # Image Preprocessing
        # ----------------------------------

        img = Image.open(filepath).convert("RGB")

        img = img.resize((128, 128))

        img_array = np.array(
            img,
            dtype=np.float32
        )

        img_array /= 255.0

        img_array = np.expand_dims(
            img_array,
            axis=0
        )

        # ----------------------------------
        # CNN Prediction
        # ----------------------------------

        predictions = MODEL.predict(
            img_array,
            verbose=0
        )

        probabilities = predictions[0]

        predicted_index = int(
            np.argmax(probabilities)
        )

        predicted_class = CLASS_NAMES[
            predicted_index
        ]

        confidence = float(
            probabilities[predicted_index]
        ) * 100
                # ==========================================
        # Top 5 Predictions
        # ==========================================

        top5_indices = np.argsort(probabilities)[-5:][::-1]

        chart_labels = []
        chart_values = []

        for index in top5_indices:

            chart_labels.append(
                CLASS_NAMES[index].replace("_", " ")
            )

            chart_values.append(
                round(
                    float(probabilities[index]) * 100,
                    2
                )
            )

        chart_data = {

            "labels": chart_labels,

            "values": chart_values

        }

        ranking = list(

            zip(
                chart_labels,
                chart_values
            )

        )

        # ==========================================
        # Default Disease Information
        # ==========================================

        default_info = {

            "Crop": "Unknown",

            "Disease": predicted_class,

            "Scientific_Name": "Unknown",

            "Pathogen": "Unknown",

            "Pathogen_Type": "Unknown",

            "Category": "Unknown",

            "Affected_Part": "Unknown",

            "Environment": "Unknown",

            "Spread": "Unknown",

            "Description": "Information not available.",

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

            "Risk_Level": "Low",

            "Severity": "Low",

            "Recommended_Actions": []

        }

        # ==========================================
        # Get Disease Information
        # ==========================================

        info = disease_database.get(

            predicted_class,

            default_info

        )

        # ==========================================
        # Store Latest Prediction
        # ==========================================

        latest_prediction = {

            "prediction": info["Disease"],

            "confidence": f"{confidence:.2f}%",

            "info": info

        }

        # ==========================================
        # Render Result
        # ==========================================

        return render_template(

            "result.html",

            image_path=image_path,

            prediction=info["Disease"],

            confidence=f"{confidence:.2f}%",

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

@app.route("/download_report")
def download_report():

    global latest_prediction

    if not latest_prediction:

        return render_template(
            "error.html",
            error="No prediction available. Please analyze an image first."
        )

    try:

        with tempfile.NamedTemporaryFile(
            delete=False,
            suffix=".pdf"
        ) as temp_file:

            pdf_path = temp_file.name

        generate_pdf(

            output_path=pdf_path,

            info=latest_prediction["info"],

            prediction=latest_prediction["prediction"],

            confidence=latest_prediction["confidence"]

        )

        return send_file(

            pdf_path,

            as_attachment=True,

            download_name="Plant_Disease_Report.pdf",

            mimetype="application/pdf"

        )

    except Exception as e:

        traceback.print_exc()

        return render_template(

            "error.html",

            error=f"Failed to generate PDF: {str(e)}"

        )


# ==========================================
# Run Flask App
# ==========================================

if __name__ == "__main__":

    app.run(debug=True)