# Smart-Agriculture-Disease-Advisor
AI-powered Smart Agriculture Disease Advisor built using Python, TensorFlow, OpenCV, Flask, MySQL, and Google Colab for crop disease detection, diagnosis, and treatment recommendations using deep learning and computer vision.

## 📌 Project Progress

- [x] Project Setup
- [x] Dataset Download
- [x] Data Exploration
- [x] Data Preprocessing
- [x] CNN Model Training
- [x] Model Evaluation
- [x] Disease Prediction
- [ ] Flask Web Application
- [ ] Database Integration
- [ ] Deployment

### ✔️ CNN Model Training

- Built a Convolutional Neural Network (CNN) using TensorFlow/Keras.
- Trained the model on the PlantVillage dataset.
- Applied image normalization and optimized the data pipeline.
- Used EarlyStopping and ModelCheckpoint callbacks.
- Saved the trained model for future inference and deployment.

### ✔️ Model Evaluation

The trained CNN model was evaluated using the PlantVillage validation dataset.

**Evaluation includes:**
- Validation accuracy and loss
- Classification report
- Confusion matrix
- Sample prediction visualization
- Performance analysis

The evaluation results demonstrate the effectiveness of the CNN model in identifying multiple plant diseases across different crop species.

### ✔️ Disease Prediction

The trained CNN model performs disease prediction on unseen plant leaf images.

**Features:**
- Upload a plant leaf image
- Automatic image preprocessing
- CNN-based disease prediction
- Confidence score estimation
- Prediction result visualization
- Supports all 38 disease classes from the PlantVillage dataset
