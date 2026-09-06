"""
Inference Validation & Benchmark Tool
Smart Agriculture Disease Advisor

Compares predictions, confidence distributions, and memory usage between
the baseline Keras model (`plant_disease_cnn.keras`) and the optimized
TensorFlow Lite model (`plant_disease_cnn.tflite`).
"""

import os
import sys
import time
import numpy as np
from PIL import Image

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODELS_DIR = os.path.join(BASE_DIR, "..", "models")
KERAS_PATH = os.path.join(MODELS_DIR, "plant_disease_cnn.keras")
TFLITE_PATH = os.path.join(MODELS_DIR, "plant_disease_cnn.tflite")


def get_memory_mb():
    try:
        import psutil
        process = psutil.Process(os.getpid())
        return process.memory_info().rss / (1024 * 1024)
    except Exception:
        return 0.0


def validate_inference(num_samples=25):
    print("=" * 60)
    print("CNN INFERENCE ACCURACY & MEMORY BENCHMARK")
    print("=" * 60)

    start_mem = get_memory_mb()
    print(f"Process Initial Memory: {start_mem:.2f} MB")

    # 1. LiteRT / TFLite Interpreter
    print("\n[1] Initializing TFLite Interpreter...")
    try:
        from ai_edge_litert.interpreter import Interpreter
    except ImportError:
        try:
            from tensorflow.lite.python.interpreter import Interpreter
        except ImportError:
            import tensorflow as tf
            Interpreter = tf.lite.Interpreter

    tflite_interp = Interpreter(model_path=TFLITE_PATH, num_threads=2)
    tflite_interp.allocate_tensors()
    in_idx = tflite_interp.get_input_details()[0]["index"]
    out_idx = tflite_interp.get_output_details()[0]["index"]
    tflite_mem = get_memory_mb()
    print(f"   TFLite Loaded Memory: {tflite_mem:.2f} MB (Delta: {tflite_mem - start_mem:.2f} MB)")

    # 2. Baseline Keras Model
    print("\n[2] Loading Baseline Keras Model...")
    try:
        import tensorflow as tf
        keras_model = tf.keras.models.load_model(KERAS_PATH, compile=False)
        keras_mem = get_memory_mb()
        print(f"   Keras Loaded Memory: {keras_mem:.2f} MB (Delta: {keras_mem - start_mem:.2f} MB)")
    except Exception as e:
        print(f"   [INFO] Keras model load skipped: {e}")
        keras_model = None

    # 3. Generate structured test patterns
    np.random.seed(42)
    top1_agreements = 0
    top5_agreements = 0
    max_conf_diff = 0.0
    sum_conf_diff = 0.0
    tflite_latencies = []

    print(f"\n[3] Running Inference on {num_samples} Sample Inputs...")
    for i in range(num_samples):
        # Create varied synthetic leaf image patterns
        raw_arr = np.random.randint(20, 240, (128, 128, 3), dtype=np.uint8)
        norm_arr = np.expand_dims(raw_arr.astype(np.float32) / 255.0, axis=0)

        # TFLite inference
        t0 = time.perf_counter()
        tflite_interp.set_tensor(in_idx, norm_arr)
        tflite_interp.invoke()
        tflite_pred = tflite_interp.get_tensor(out_idx)[0]
        t1 = time.perf_counter()
        tflite_latencies.append((t1 - t0) * 1000)

        if keras_model is not None:
            keras_pred = keras_model.predict(norm_arr, verbose=0)[0]
            k_top1 = int(np.argmax(keras_pred))
            t_top1 = int(np.argmax(tflite_pred))

            k_top5 = set(np.argsort(keras_pred)[-5:])
            t_top5 = set(np.argsort(tflite_pred)[-5:])

            if k_top1 == t_top1:
                top1_agreements += 1
            if k_top5 == t_top5:
                top5_agreements += 1

            conf_diff = abs(float(keras_pred[k_top1]) - float(tflite_pred[t_top1]))
            max_conf_diff = max(max_conf_diff, conf_diff)
            sum_conf_diff += conf_diff

    peak_mem = get_memory_mb()
    print("\n" + "=" * 60)
    print("VALIDATION & BENCHMARK RESULTS")
    print("=" * 60)
    print(f"Total Samples Evaluated  : {num_samples}")
    if keras_model is not None:
        print(f"Top-1 Agreement          : {top1_agreements}/{num_samples} ({top1_agreements/num_samples*100:.1f}%)")
        print(f"Top-5 Agreement          : {top5_agreements}/{num_samples} ({top5_agreements/num_samples*100:.1f}%)")
        print(f"Max Confidence Diff      : {max_conf_diff:.6f}")
        print(f"Avg Confidence Diff      : {sum_conf_diff/num_samples:.6f}")
    print(f"Average TFLite Latency   : {np.mean(tflite_latencies):.2f} ms")
    print(f"Peak Process Memory      : {peak_mem:.2f} MB")
    print("=" * 60)


if __name__ == "__main__":
    validate_inference()
