"""
Model Conversion Tool: Keras to TensorFlow Lite (Float16 Quantization)
Smart Agriculture Disease Advisor

Converts the baseline trained Keras CNN model (`plant_disease_cnn.keras`)
into a lightweight, optimized TensorFlow Lite model (`plant_disease_cnn.tflite`).
"""

import os
import sys

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODELS_DIR = os.path.join(BASE_DIR, "..", "models")
KERAS_PATH = os.path.join(MODELS_DIR, "plant_disease_cnn.keras")
TFLITE_PATH = os.path.join(MODELS_DIR, "plant_disease_cnn.tflite")


def convert_keras_to_tflite(keras_model_path=KERAS_PATH, tflite_model_path=TFLITE_PATH):
    print("=" * 60)
    print("CONVERTING KERAS CNN MODEL TO TENSORFLOW LITE (FLOAT16)")
    print("=" * 60)

    if not os.path.exists(keras_model_path):
        print(f"[ERROR] Keras model file not found at '{keras_model_path}'")
        sys.exit(1)

    try:
        import tensorflow as tf
    except ImportError:
        print("[ERROR] TensorFlow is required for model conversion. Install tensorflow in your development environment.")
        sys.exit(1)

    print(f"Loading baseline Keras model from: {keras_model_path}")
    keras_model = tf.keras.models.load_model(keras_model_path, compile=False)
    keras_size_mb = os.path.getsize(keras_model_path) / (1024 * 1024)
    print(f"   Original Model Size: {keras_size_mb:.2f} MB")
    print(f"   Total Parameters: {keras_model.count_params():,}")

    print("Setting up TFLite Converter with Float16 quantization...")
    converter = tf.lite.TFLiteConverter.from_keras_model(keras_model)
    converter.optimizations = [tf.lite.Optimize.DEFAULT]
    converter.target_spec.supported_types = [tf.float16]

    print("Performing conversion...")
    tflite_model = converter.convert()

    os.makedirs(os.path.dirname(tflite_model_path), exist_ok=True)
    with open(tflite_model_path, "wb") as f:
        f.write(tflite_model)

    tflite_size_mb = os.path.getsize(tflite_model_path) / (1024 * 1024)
    compression = (1 - (tflite_size_mb / keras_size_mb)) * 100

    print(f"[SUCCESS] Converted model saved to: {tflite_model_path}")
    print(f"   Optimized TFLite Size: {tflite_size_mb:.2f} MB")
    print(f"   Compression Ratio: {compression:.2f}% reduction")
    print("=" * 60)


if __name__ == "__main__":
    convert_keras_to_tflite()
