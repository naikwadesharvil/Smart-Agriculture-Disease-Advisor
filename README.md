# 🌿 Smart Agriculture Disease Advisor

> **AI-powered plant disease detection, diagnosis, agronomic insights, treatment recommendations, and downloadable PDF advisory reports using deep learning and computer vision.**

[![Python](https://img.shields.io/badge/Python-3.12-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-3.x-000000?logo=flask&logoColor=white)](https://flask.palletsprojects.com/)
[![TensorFlow Lite](https://img.shields.io/badge/Model-TFLite%20FP16-FF6F00?logo=tensorflow&logoColor=white)](https://www.tensorflow.org/lite)
[![Deployment](https://img.shields.io/badge/Render-Live%20Production-46E3B7?logo=render&logoColor=white)](https://smart-agriculture-disease-advisor.onrender.com)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

---

## 🌐 Live Demo

### 🚀 [Open Smart Agriculture Disease Advisor](https://smart-agriculture-disease-advisor.onrender.com)

- **Live Application:** [https://smart-agriculture-disease-advisor.onrender.com](https://smart-agriculture-disease-advisor.onrender.com)
- **GitHub Repository:** [https://github.com/naikwadesharvil/Smart-Agriculture-Disease-Advisor](https://github.com/naikwadesharvil/Smart-Agriculture-Disease-Advisor)

---

## 📖 Project Overview

**Smart Agriculture Disease Advisor** is an end-to-end artificial intelligence agricultural decision-support platform designed to assist farmers, agronomists, and researchers in rapidly identifying plant diseases from leaf imagery.

Trained on the **PlantVillage dataset**, the underlying Convolutional Neural Network (CNN) recognizes **38 distinct classes** (diseases and healthy foliage) across **14 major crop species**. In addition to classifying pathology, the system delivers structured agronomic advisory profiles—including pathogen types, symptoms, biological causes, disease progression cycles, organic treatments, chemical controls, and preventative management strategies.

---

## ✨ Key Features

- **🔬 38-Class Plant Pathology Recognition**: High-precision multi-class image classification covering 14 crop species.
- **⚡ Lightweight Production Inference**: Powered by **TensorFlow Lite (Float16 quantized)** and `ai-edge-litert` for fast CPU execution (~14 ms) with minimal memory footprint (~106 MB peak RSS).
- **📊 Top-5 Prediction Distribution**: Interactive probability ranking and confidence scoring powered by Chart.js.
- **📚 Comprehensive Disease Knowledge Base**: Structured JSON-backed repository of causes, environmental drivers, organic therapies, recommended chemical agents, and prevention guidelines.
- **📄 Downloadable PDF Advisory Reports**: Automated 3-page, publication-quality A4 Portrait diagnostic reports with embedded leaf images, disease progression timelines, and risk assessments.
- **📜 Diagnostic History Log**: Client-side prediction archive with individual record inspection and one-click history clearing.
- **🌓 Modern Responsive UI**: Clean agricultural aesthetic with dark mode support, drag-and-drop file upload, and live image preview.
- **🛡️ Production-Grade Security**: Input validation, 16 MB upload restriction, strict filename sanitization, HTTP security headers, and shielded error pages.

---

## 🛠️ Technology Stack

| Layer | Technologies |
|---|---|
| **Deep Learning & Inference** | **TensorFlow Lite (FP16 Quantized)**, `ai-edge-litert`, NumPy, Pillow, TensorFlow/Keras *(Original Research Model)* |
| **Backend Framework** | **Python 3.12**, **Flask 3.x**, Werkzeug |
| **Report Generation** | **ReportLab** (Platypus Flowables, Dynamic Two-Pass Canvas) |
| **Frontend & UI** | **HTML5**, **CSS3**, **JavaScript (ES6+)**, **Bootstrap 5**, **Bootstrap Icons**, **AOS** |
| **Data Visualization** | **Chart.js** |
| **Database & Persistence** | **JSON Structured Storage** (`disease_database.json`, `prediction_history.json`) |
| **WSGI Server & Cloud** | **Gunicorn**, **Render** |

---

## 📁 Project Structure

```text
Smart-Agriculture-Disease-Advisor/
├── app/
│   ├── app.py                      # Main Flask application, routes & inference pipeline
│   ├── history.py                  # Diagnostic history management helper
│   ├── pdf_generator.py            # ReportLab PDF report generation engine
│   ├── prediction_history.json     # Local prediction history storage
│   ├── weather.py                  # Agronomic weather helper
│   ├── static/
│   │   ├── css/
│   │   │   └── style.css           # Custom stylesheets & Dark Mode tokens
│   │   ├── js/
│   │   │   ├── main.js             # UI interactions, theme toggle & drag-and-drop
│   │   │   └── dashboard.js        # Chart.js Top-5 probability distribution
│   │   ├── images/                 # Static brand assets (hero, about, guide, logo)
│   │   └── uploads/                # Processed leaf image directory (.gitkeep)
│   └── templates/
│       ├── base.html               # Master layout template (Navbar, Footer, Theme)
│       ├── index.html              # Home page with upload dropzone & workflow
│       ├── result.html             # Detailed diagnostic dashboard & charts
│       ├── history.html            # Prediction history archive table
│       ├── about.html              # System architecture & model methodology
│       ├── guide.html              # Farmer practical usage guidelines
│       └── error.html              # Custom error shielding page (400, 404, 500, etc.)
├── database/
│   ├── disease_database.json       # Authoritative 38-class agronomic knowledge base
│   └── validate_database.py        # Schema & key consistency verification script
├── models/
│   ├── plant_disease_cnn.keras     # Original full-precision CNN model (Git LFS)
│   └── plant_disease_cnn.tflite    # Optimized Float16 TFLite production model (12.45 MB)
├── notebooks/                      # Exploratory data analysis & CNN training notebooks
├── tools/
│   ├── convert_model.py            # Float16 TFLite quantization conversion script
│   └── validate_inference.py       # Dual-engine validation & agreement test script
├── .env.example                    # Environment variable configuration template
├── .gitignore                      # Git exclusion rules
├── .python-version                 # Pinned Python version (3.12)
├── LICENSE                         # MIT License
├── Procfile                        # Cloud WSGI process definition (Gunicorn)
├── requirements.txt                # Production dependencies
└── README.md                       # Project documentation
```

---

## 🌿 Supported Crops & Diseases (38 Classes)

The system supports accurate diagnosis across **14 plant species**:

- **Apple**: Apple Scab, Black Rot, Cedar Apple Rust, Healthy
- **Blueberry**: Healthy
- **Cherry**: Powdery Mildew, Healthy
- **Corn (Maize)**: Cercospora Leaf Spot / Gray Leaf Spot, Common Rust, Northern Leaf Blight, Healthy
- **Grape**: Black Rot, Esca (Black Measles), Leaf Blight (Isariopsis Leaf Spot), Healthy
- **Orange**: Huanglongbing (Citrus Greening)
- **Peach**: Bacterial Spot, Healthy
- **Pepper (Bell)**: Bacterial Spot, Healthy
- **Potato**: Early Blight, Late Blight, Healthy
- **Raspberry**: Healthy
- **Soybean**: Healthy
- **Squash**: Powdery Mildew
- **Strawberry**: Leaf Scorch, Healthy
- **Tomato**: Bacterial Spot, Early Blight, Late Blight, Leaf Mold, Septoria Leaf Spot, Spider Mites, Target Spot, Tomato Yellow Leaf Curl Virus, Tomato Mosaic Virus, Healthy

---

## ⚙️ Prediction Workflow

```
[ User Uploads Leaf Image ]
            │
            ▼
[ File Validation & Security Checks ] ── (Size ≤ 16MB, MIME, Pillow Integrity)
            │
            ▼
[ Image Preprocessing ] ───────────────── (RGB Conversion, 128×128 Resize, 1/255.0 Normalization)
            │
            ▼
[ Lazy Model Initialization ] ────────── (Thread-safe on-demand loader via threading.Lock)
            │
            ▼
[ TFLite Engine Inference ] ──────────── (ai-edge-litert CPU execution, ~14 ms latency)
            │
            ▼
[ Probability Distribution ] ─────────── (38-class Softmax probabilities & Top-5 extraction)
            │
            ▼
[ Agronomic Knowledge Lookup ] ───────── (Symptoms, Causes, Organic/Chemical Controls, Risk)
            │
            ▼
[ UI Dashboard & Chart.js Rendering ]
            │
            ▼
[ Export PDF Diagnostic Report ] ─────── (A4 Portrait, 3 Pages, Dynamic Canvas Numbering)
```

1. **Upload**: User submits a plant leaf photo (`.jpg`, `.jpeg`, `.png`) via drag-and-drop or file selector.
2. **Validation**: Server validates file format, MIME type, file size boundary (16 MB limit), and image header integrity.
3. **Preprocessing**: Image is transformed to RGB, resized to $128 \times 128$ pixels, and normalized ($1/255.0$).
4. **Lazy Initialization**: The production TFLite model is loaded into memory on-demand upon the first inference call.
5. **Inference**: `ai-edge-litert` executes low-latency inference on the Float16 model.
6. **Classification**: 38-class softmax probabilities are generated.
7. **Visualization**: Top-5 predicted conditions, confidence scores, and probability bar charts are rendered via Chart.js.
8. **Advisory Retrieval**: Detailed disease profiles (pathogen, spread vectors, symptoms, causes, organic treatments, chemical controls, progression stages) are retrieved from `disease_database.json`.
9. **History Logging**: Diagnosis metadata is appended to local diagnostic history.
10. **Report Export**: User can generate and download a publication-grade PDF report.

---

## ⚡ Production Model Optimization & Benchmarks

To ensure high availability and responsiveness on constrained cloud instances (such as the Render Free Tier with 512 MB RAM), the original 74.7 MB Keras CNN model was converted to an optimized **Float16 TensorFlow Lite** model:

| Metric | Original Keras Model | Production TFLite Model | Optimization Impact |
|---|---|---|---|
| **Model Format** | `.keras` (Float32) | `.tflite` (Float16 Quantized) | **83.3% Smaller** |
| **File Size** | ~74.73 MB | **~12.45 MB** | Lightweight disk footprint |
| **Inference Engine** | Full TensorFlow 2.x | **ai-edge-litert** | Heavy runtime eliminated |
| **Idle Memory (RSS)** | ~360 MB | **~31.5 MB** | **91.3% Idle RAM Reduction** |
| **Peak Inference RAM** | ~385 MB | **~106.57 MB** | Safe under 512 MB RAM limits |
| **Inference Latency** | ~210 ms | **~14 ms** | **15× Faster Execution** |
| **Top-1 / Top-5 Agreement** | Baseline (100%) | **100.0% Agreement** | Zero classification degradation |
| **Confidence Variance** | Baseline | **< 0.18% average** | Statistically negligible delta |

> *Note: Memory and latency values represent benchmark measurements under Linux x86_64 container environments.*

---

## 📄 PDF Advisory Report

The application generates comprehensive, structured diagnostic reports formatted with ReportLab Platypus:

- **Format & Geometry**: Strict **A4 Portrait** ($210\text{ mm} \times 297\text{ mm}$ / $595.28\text{ pt} \times 841.89\text{ pt}$) with consistent 18 mm margins.
- **Page Layout**: Exactly **3 balanced pages** verified across all 38 disease categories.
- **Page 1**: Report Header, Uploaded Leaf Image (aspect-ratio preserved), Prediction Summary, Disease Description, Disease Profile (Pathogen, Spread, Environment), and Primary Symptoms.
- **Page 2**: Detailed Causes, Primary Treatments, Organic Controls, Recommended Chemical Agents, Prevention Protocols, and Actionable Steps.
- **Page 3**: Disease Progression Timeline (Early, Moderate, Severe, Estimated Duration), Risk & Advisory Summary (Diagnostic Target, AI Confidence, Pathology Risk, Clinical Severity, Monitoring Urgency), and Key Recommendations.
- **Footer**: Distinct footer featuring document title, **"Made By Sharvil"** author credit, dynamic `"Page X of 3"` pagination, and top border rule.

---

## 🚀 Installation & Local Setup

### 1. Clone the Repository
```bash
git clone https://github.com/naikwadesharvil/Smart-Agriculture-Disease-Advisor.git
cd Smart-Agriculture-Disease-Advisor
```

### 2. Create and Activate a Virtual Environment

**On Windows (PowerShell):**
```powershell
python -m venv .venv
.venv\Scripts\activate
```

**On Linux / macOS:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Configure Environment Variables (Optional)
```bash
# On Windows:
copy .env.example .env

# On Linux / macOS:
cp .env.example .env
```

### 5. Run the Application

**Development Server:**
```bash
python app/app.py
```
Access the application locally at `http://127.0.0.1:5000/`.

**Production Server (Gunicorn):**
```bash
gunicorn --workers 1 --threads 2 --timeout 120 --bind 0.0.0.0:5000 app.app:app
```

---

## 🌐 Deployment Guidelines

- **Runtime**: Python 3.12 pinned via `.python-version`.
- **Hosting Platform**: [Render](https://render.com) (Web Service).
- **Process Manager**: Gunicorn WSGI configured via `Procfile`:
  ```text
  web: gunicorn --workers 1 --threads 2 --timeout 120 --bind 0.0.0.0:$PORT app.app:app
  ```
- **Concurrency & Memory Model**: A single worker with two threads ensures low memory consumption during concurrent requests.
- **Health Check**: Dedicated lightweight `GET /health` endpoint for load balancers and container monitoring without triggering model initialization.

### ☁️ Deployment Notes & Persistence
Cloud platforms such as Render Free Tier and container runtimes utilize **ephemeral filesystems**. Uploaded images in `app/static/uploads/` and history in `prediction_history.json` persist during container uptime and reset upon container restart. For persistent multi-tenant deployments, connect an external managed database (e.g. PostgreSQL) and cloud object storage (e.g. AWS S3 or Google Cloud Storage).

---

## 🔒 Security & Hardening

- **Filename Sanitization**: Uploaded files receive cryptographic random tokens (`UUID4` prefix + timestamp + `secure_filename`) preventing overwrite collisions and directory traversal.
- **Image Integrity Verification**: Uploaded files are verified via Pillow image decoders; invalid or corrupted files are immediately rejected and purged.
- **Size Boundary**: 16 MB maximum content length enforced at the framework level.
- **Security Headers**: Custom middleware injects `X-Content-Type-Options: nosniff`, `X-Frame-Options: SAMEORIGIN`, and `Referrer-Policy: strict-origin-when-cross-origin`.
- **Error Shielding**: Custom error templates (`error.html`) handle 400, 404, 405, 413, and 500 error codes without leaking server stack traces or internal paths.
- **Secret Isolation**: Sensitive parameters managed through environment variables; local credentials excluded via `.gitignore`.

---

## 🧪 Verification & Testing

The project is thoroughly verified through automated regression suites:

- **Health Endpoint**: `GET /health` returns HTTP 200 `{"status": "healthy"}`.
- **Core Navigation**: `GET /`, `/about`, `/guide`, `/history` verified for valid HTML rendering.
- **Inference Pipeline**: `POST /predict` verified with valid and invalid payloads.
- **PDF Report Generation**: `GET /download_report` verified across all 38 disease classes for A4 Portrait geometry, 3-page layout, and "Made By Sharvil" footer.
- **Dual-Model Parity**: Verified with `tools/validate_inference.py` ensuring 100% Top-1 and Top-5 class parity between `.keras` and `.tflite`.

---

## 👨‍💻 Author

**Made By Sharvil**  
[Sharvil Naikwade](https://github.com/naikwadesharvil)  
*Smart Agriculture Disease Advisor*

---

## 📄 License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.
