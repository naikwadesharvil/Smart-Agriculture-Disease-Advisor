# Smart-Agriculture-Disease-Advisor

AI-powered Smart Agriculture Disease Advisor built using Python, TensorFlow/Keras, Flask, HTML, CSS, JavaScript, Bootstrap, and JSON for crop disease detection, diagnosis, and treatment recommendations using deep learning and computer vision.

## 📌 Project Progress

- [x] Project Setup
- [x] Dataset Download
- [x] Data Exploration
- [x] Data Preprocessing
- [x] CNN Model Training
- [x] Model Evaluation
- [x] Disease Prediction
- [x] Disease Knowledge Base
- [x] Flask Web Application
- [x] Disease Information Dashboard
- [x] Prediction Confidence Analysis
- [x] Top-5 Prediction Visualization
- [x] Treatment Recommendations
- [x] Organic Treatment Recommendations
- [x] Disease Prevention Information
- [x] Risk and Severity Assessment
- [x] PDF Report Generation
- [x] Prediction History
- [x] Responsive User Interface
- [x] Dark Mode
- [ ] Database Expansion
- [ ] Deployment

---

### ✔️ CNN Model Training

- Built a Convolutional Neural Network (CNN) using TensorFlow/Keras.
- Trained the model on the PlantVillage dataset.
- Applied image normalization and preprocessing.
- Resized input images to `128 × 128`.
- Used EarlyStopping and ModelCheckpoint callbacks.
- Saved the trained model for future inference and deployment.
- The model supports **38 plant disease classes**.

---

### ✔️ Model Evaluation

The trained CNN model was evaluated using the PlantVillage validation dataset.

**Evaluation includes:**

- Validation accuracy and loss
- Classification report
- Confusion matrix
- Sample prediction visualization
- Performance analysis

The evaluation results demonstrate the effectiveness of the CNN model in identifying multiple plant diseases across different crop species.

---

### ✔️ Disease Prediction

The trained CNN model performs disease prediction on unseen plant leaf images.

**Features:**

- Upload a plant leaf image
- Supports JPG, JPEG, and PNG images
- Automatic image preprocessing
- RGB conversion
- Image resizing to `128 × 128`
- Pixel normalization
- CNN-based disease prediction
- Confidence score estimation
- Top-5 prediction analysis
- Prediction result visualization
- Supports 38 disease classes

---

### ✔️ Disease Knowledge Base

A structured disease knowledge base was developed to complement the AI prediction model.

The knowledge base is stored in:

```text
database/disease_database.json
