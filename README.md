# 🧠 Sign Language to Audio Converter

A real-time computer vision project that detects sign language gestures using a webcam and converts them into spoken audio.  
The goal is to bridge communication between sign language users and non-signers using AI.

---

## 🚀 Features

- 📷 Real-time hand detection using webcam  
- ✋ Gesture recognition using ML model  
- 📝 Converts gestures → text  
- 🔊 Converts text → speech output  
- ⚡ Lightweight and runs locally  
- 📦 Easy to extend for mobile or web apps  

---

## 🛠️ Tech Stack

- **Python**
- **OpenCV** – video capture & processing  
- **MediaPipe** – hand tracking & landmarks  
- **Scikit-learn / ML model** – gesture classification  
- **pyttsx3** – text to speech  

---

## 🧩 Project Workflow

1. Capture hand gestures via webcam  
2. Extract 21 hand landmarks using MediaPipe  
3. Feed landmark data into trained ML model  
4. Predict gesture → convert to text  
5. Convert text → speech output  



---

## 📁 Project Structure

sign-language-audio/
│
├── dataset/ # Collected gesture data
├── models/ # Trained ML model
│
├── collect.py # Dataset collection script
├── train_model.py # Model training
├── predict.py # Live gesture detection
├── tts.py # Text-to-speech module
│
└── README.md


---

## ⚙️ Installation

### 1️⃣ Clone the repository

```bash
git clone https://github.com/Reaven010/sign-language-audio.git
cd sign-language-audio

---

##pip install opencv-python mediapipe scikit-learn pyttsx3 numpy
