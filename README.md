# Smart-Agriculture-Disease-Advisor

AI-powered Smart Agriculture Disease Advisor built using Python, TensorFlow/Keras, Flask, HTML, CSS, JavaScript, Bootstrap, and JSON for plant disease detection, comprehensive diagnosis, agronomic insights, and treatment recommendations using deep learning and computer vision.

---

## 📌 Project Highlights & Features

- **38-Class Plant Disease Recognition**: Trained on the PlantVillage dataset covering 14 crop species.
- **Deep Learning CNN Pipeline**: Real-time inference with softmax confidence and Top-5 class probability distributions.
- **Comprehensive Agronomic Knowledge Base**: Structured JSON database providing symptoms, causes, organic treatments, chemical controls, and prevention tips for all 38 classes.
- **Interactive Web Interface**: Responsive design with Dark Mode, drag-and-drop file upload, live image preview, and animated probability charts (Chart.js).
- **PDF Advisory Reports**: Automated downloadable PDF diagnostic reports with embedded leaf images, generated via ReportLab.
- **Diagnostic History Log**: Client-accessible prediction history log with single-record and full-history management.
- **Production-Ready Hardening**: Security headers (`nosniff`, `SAMEORIGIN`, `strict-origin-when-cross-origin`), safe upload validation, 16 MB upload boundary, and environment variable configuration.

---

## 🛠️ Technology Stack

| Layer | Technology |
|---|---|
| **Deep Learning** | TensorFlow 2.x, Keras, NumPy, Pillow |
| **Backend Framework** | Python 3.10+, Flask 3.x, Werkzeug |
| **Report Generation** | ReportLab |
| **Frontend & Styling** | HTML5, CSS3, JavaScript (ES6+), Bootstrap 5, Bootstrap Icons |
| **Data Visualization** | Chart.js, AOS (Animate On Scroll) |
| **Knowledge Base & Persistence** | JSON-based structured storage |
| **Production Server** | Gunicorn / Waitress (WSGI) |

---

## 📁 Project Structure

```text
Smart-Agriculture-Disease-Advisor/
├── app/
│   ├── app.py                      # Core Flask web application & API routes
│   ├── history.py                  # Prediction history management
│   ├── pdf_generator.py            # PDF advisory report generation engine
│   ├── prediction_history.json     # Local JSON history storage
│   ├── weather.py                  # Weather integration helper (optional)
│   ├── static/
│   │   ├── css/
│   │   │   └── style.css           # Custom styles & dark mode design tokens
│   │   ├── js/
│   │   │   ├── main.js             # Theme toggle, drag-and-drop, UI handlers
│   │   │   └── dashboard.js        # Chart.js Top-5 visualization logic
│   │   ├── images/                 # UI assets (hero, about, guide, logo)
│   │   └── uploads/                # Processed leaf image directory (.gitkeep)
│   └── templates/
│       ├── base.html               # Master layout with navbar, footer, & theme switch
│       ├── index.html              # Home page with upload zone & workflow steps
│       ├── result.html             # Detailed diagnosis dashboard & charts
│       ├── history.html            # Diagnostic history records table
│       ├── about.html              # Project overview & architecture page
│       ├── guide.html              # Farmer usage guidelines & instructions
│       ├── error.html              # Robust error page (400, 404, 405, 413, 500)
│       └── components/             # Reusable Jinja template components
├── database/
│   ├── disease_database.json       # 38-class plant disease knowledge base
│   └── validate_database.py        # Database schema verification script
├── models/
│   └── plant_disease_cnn.keras     # Trained CNN model
├── notebooks/                      # Exploratory data analysis & model training notebooks
├── .env.example                    # Environment variable template
├── .gitignore                      # Git exclusion rules
├── requirements.txt                # Python package dependencies
└── README.md                       # Documentation
```

---

## 🌿 Supported Crops & Diseases (38 Classes)

The CNN model supports diagnosis across 14 plant species:
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

## 🚀 Installation & Local Setup

### 1. Clone the Repository
```bash
git clone https://github.com/naikwadesharvil/Smart-Agriculture-Disease-Advisor.git
cd Smart-Agriculture-Disease-Advisor
```

### 2. Create and Activate a Virtual Environment

**On Windows (PowerShell / Command Prompt):**
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
Copy the example environment file:
```bash
# On Windows:
copy .env.example .env

# On Linux / macOS:
cp .env.example .env
```

Set appropriate configuration in `.env`:
```ini
SECRET_KEY=your-custom-secret-key
FLASK_DEBUG=1
HOST=127.0.0.1
PORT=5000
```

### 5. Run the Application

**Development Mode:**
```bash
python app/app.py
```
Open your browser and navigate to `http://127.0.0.1:5000/`.

**Production Mode (WSGI on Linux / Cloud Container):**
```bash
gunicorn --workers 1 --threads 2 --timeout 120 --bind 0.0.0.0:$PORT app.app:app
```
> **Note for 512 MB RAM Instances (e.g. Render Free Tier):**
> Use `--workers 1 --threads 2` to ensure only a single TensorFlow model instance is loaded into memory (~360–380 MB RSS), avoiding container memory crashes (HTTP 502 / OOM).

**Production Mode on Windows:**
```bash
waitress-serve --listen=0.0.0.0:5000 app.app:app
```

---

## 📊 Prediction Workflow

1. **Upload**: User submits a plant leaf photo (`.jpg`, `.jpeg`, `.png`) via drag-and-drop or file picker.
2. **Validation**: Integrity checks verify extension, MIME type, file size (max 16 MB), and Pillow image validity.
3. **Preprocessing**: The image is converted to RGB, resized to `128 × 128` pixels, and normalized (`1/255.0`).
4. **CNN Inference**: The TensorFlow model computes class probabilities across all 38 categories in ~180 ms.
5. **Knowledge Base Lookup**: Agronomic metadata is retrieved from `disease_database.json`.
6. **Dashboard Visualization**: Results, risk ratings, organic remedies, chemicals, and Top-5 probability charts are displayed.
7. **Export & History**: Diagnosis is appended to history and a comprehensive PDF advisory report can be downloaded.

---

## 🌐 Deployment Architecture & Guidelines

### Recommended Deployment Platforms
- **Render / Railway / Fly.io**: Deploy as a Web Service running Python 3.12 with Gunicorn (`--workers 1 --threads 2 --timeout 120`).
- **Health Check Endpoint**: `GET /health` returns `{"status": "healthy"}` with HTTP 200.
- **Docker-based Hosting (AWS ECS / GCP Cloud Run / Azure Container Apps)**: Containerize the Flask application with Python 3.12 base image.

### ⚠️ Storage & Persistence Considerations
- **Ephemeral Filesystem**: Platforms such as Render Free Tier and Cloud Run use ephemeral disk storage. Any uploaded images in `app/static/uploads/` and history in `prediction_history.json` will reset upon container restart.
- For multi-instance production environments requiring permanent record retention, consider mounting a cloud volume or backing history with a managed database (PostgreSQL/MySQL) and uploads with S3/GCS.

---

## 🔒 Security & Safe Operation

- **Input Validation**: Strict filename sanitization (`secure_filename` + timestamp + UUID token) prevents overwrite collisions and path traversal.
- **Memory & Resource Safety**: Images and temporary PDF descriptors are deterministically managed via context managers.
- **HTTP Security Headers**: Native middleware adds `X-Frame-Options`, `X-Content-Type-Options: nosniff`, and `Referrer-Policy`.
- **Error Shielding**: User-facing custom error templates prevent internal stack trace and server environment exposure.

---

## 📄 License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.
