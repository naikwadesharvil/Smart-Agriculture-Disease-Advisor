import json
import os
from datetime import datetime


# ==========================================
# History Configuration
# ==========================================

BASE_DIR = os.path.dirname(
    os.path.abspath(__file__)
)

HISTORY_FILE = os.path.join(
    BASE_DIR,
    "prediction_history.json"
)


# ==========================================
# Load History
# ==========================================

def load_history():

    if not os.path.exists(HISTORY_FILE):
        return []

    try:

        with open(
            HISTORY_FILE,
            "r",
            encoding="utf-8"
        ) as file:

            data = json.load(file)

        if isinstance(data, list):
            return data

        return []

    except (
        json.JSONDecodeError,
        OSError
    ):

        return []


# ==========================================
# Save History
# ==========================================

def save_history(history):

    try:

        with open(
            HISTORY_FILE,
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                history,
                file,
                indent=4,
                ensure_ascii=False
            )

        return True

    except OSError:

        return False


# ==========================================
# Add Prediction
# ==========================================

def add_prediction(
    prediction,
    confidence,
    info,
    image_path=None
):

    history = load_history()


    # ======================================
    # Create History Entry
    # ======================================

    entry = {

        "id": len(history) + 1,

        "timestamp":
            datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            ),

        "prediction": prediction,

        "confidence": confidence,

        "image_path": image_path,

        "crop": info.get(
            "Crop",
            "Unknown"
        ),

        "disease": info.get(
            "Disease",
            prediction
        ),

        "scientific_name": info.get(
            "Scientific_Name",
            "Unknown"
        ),

        "risk_level": info.get(
            "Risk_Level",
            "Unknown"
        ),

        "severity": info.get(
            "Severity",
            "Unknown"
        )

    }


    # ======================================
    # Add To History
    # ======================================

    history.append(entry)


    # ======================================
    # Save
    # ======================================

    save_history(history)


    return entry


# ==========================================
# Get All Predictions
# ==========================================

def get_history():

    return load_history()


# ==========================================
# Get Latest Prediction
# ==========================================

def get_latest_prediction():

    history = load_history()


    if not history:
        return None


    return history[-1]


# ==========================================
# Clear History
# ==========================================

def clear_history():

    return save_history([])


# ==========================================
# Delete Single History Entry
# ==========================================

def delete_prediction(
    prediction_id
):

    history = load_history()


    updated_history = [

        item

        for item in history

        if item.get("id") != prediction_id

    ]


    # Re-number IDs

    for index, item in enumerate(
        updated_history,
        start=1
    ):

        item["id"] = index


    save_history(
        updated_history
    )


    return updated_history