# GestureAR 🎭

### Real-Time Gesture-Based Augmented Reality Using Computer Vision

GestureAR is a real-time computer-vision application that uses **hand gestures and facial landmarks** to control augmented-reality filters through a webcam.

Instead of using a mouse, keyboard, or touchscreen, users can interact with the application using natural hand gestures.

The project combines **OpenCV, MediaPipe, NumPy, and Machine Learning** to detect gestures, track faces and hands, and render interactive AR effects in real time.

---

## ✨ Features

- 🎥 Real-time webcam processing
- ✋ Hand gesture recognition
- 😊 Face landmark detection
- 🕶️ Gesture-controlled AR filters
- 💖 Heart gesture detection
- 📸 Gesture-controlled screenshots
- ⚡ Real-time computer-vision processing
- 🧩 Modular project architecture
- 🎨 Interactive Snapchat-style AR experience

---

## 🖐️ Gesture Controls

| Gesture | Action |
|---|---|
| ✌️ Peace | Goggles filter |
| 👍 Thumbs Up | Dog filter |
| ✊ Fist | Cat filter |
| 🖐️ Open Palm | Bow filter |
| 🤟 Make Up Gesture | Makeup filter |
| 🫶 Heart Gesture | Hearts effect |
| ☝️ Index Pointing | Capture screenshot |

The application also includes a cooldown mechanism for screenshot actions to prevent continuous captures from a single gesture.

---

## 🧠 How It Works

GestureAR follows a real-time computer-vision pipeline:

```text
Webcam
   ↓
Frame Capture
   ↓
Hand + Face Detection
   ↓
Hand Landmark Extraction
   ↓
Gesture Recognition
   ↓
Gesture → AR Action
   ↓
AR Filter Rendering
   ↓
Screenshot Detection
   ↓
Display Final Frame
```

### Processing Flow

1. The webcam continuously captures frames.
2. MediaPipe detects hand and face landmarks.
3. Hand landmarks are processed to identify gestures.
4. The recognized gesture is mapped to an AR effect.
5. The filter renderer applies the corresponding visual effect.
6. The heart gesture is handled independently for the hearts effect.
7. Index-pointing detection can trigger a screenshot.
8. The processed frame is displayed in real time.

---

## 🏗️ Project Architecture

The project is organized into separate modules so that detection, gesture recognition, rendering, and camera management remain independent.

```text
GestureAI/
│
├── main.py
├── requirements.txt
├── README.md
│
├── camera/
│   ├── __init__.py
│   └── camera_manager.py
│
├── hand_tracking/
│   ├── __init__.py
│   ├── hand_detector.py
│   └── gesture_recognizer.py
│
├── face_tracking/
│   ├── __init__.py
│   └── face_detector.py
│
├── gestures/
│   ├── __init__.py
│   ├── heart_gesture.py
│   └── control_gestures.py
│
├── filter_engine/
│   ├── __init__.py
│   └── filter_renderer.py
│
├── ml/
│   ├── __init__.py
│   └── feature_extractor.py
│
├── control_mode/
│   ├── __init__.py
│   └── controller.py
│
├── assets/
│   └── AR filter assets
│
└── screenshots/
    └── captured screenshots
```

> Your exact asset files may differ depending on the filters included in your local project.

---

## 🛠️ Technologies Used

### Programming Language
- Python

### Computer Vision
- OpenCV
- MediaPipe

### Numerical Processing
- NumPy

### Machine Learning
- Scikit-learn

### Development Tools
- Visual Studio Code
- Python Virtual Environment
- Git
- GitHub

---

## 📦 Installation

### 1. Clone the repository

```bash
git clone https://github.com/mehanazshaik/GestureAI.git
```

### 2. Open the project

```bash
cd GestureAI
```

### 3. Create a virtual environment

```bash
python -m venv venv
```

### 4. Activate the environment

On Windows:

```bash
venv\Scripts\activate
```

### 5. Install dependencies

```bash
pip install -r requirements.txt
```

### 6. Run GestureAR

```bash
python main.py
```

Make sure your webcam is available and accessible to the application.

---

## 🎮 Usage

After launching the application:

1. Position yourself in front of the webcam.
2. Make one of the supported hand gestures.
3. GestureAR detects the gesture.
4. The corresponding AR filter is rendered.
5. Use the index-pointing gesture to capture a screenshot.
6. Press `Q` to close the application.

---

## 📸 Screenshots

Add screenshots of your working application here.

Example:

```text
screenshots/
├── goggles.png
├── dog_filter.png
├── cat_filter.png
├── bow_filter.png
├── makeup_filter.png
├── heart_filter.png
└── screenshot_action.png
```

You can later replace this section with actual GitHub image previews.

---

## 🎥 Demo

A short demonstration video can showcase:

```text
1. Launch GestureAR
2. Peace → Goggles
3. Thumbs Up → Dog
4. Fist → Cat
5. Open Palm → Bow
6. Make Up → Makeup
7. Heart → Hearts
8. Index → Screenshot
9. Press Q → Exit
```

---

## 💡 Problem Statement

Traditional computer interfaces rely heavily on physical input devices such as keyboards, mice, and touchscreens.

GestureAR explores a more natural form of interaction by using **computer vision and hand gestures** to control digital visual effects.

The project demonstrates how real-time vision systems can interpret human gestures and translate them into interactive computer actions.

---

## 🎯 Project Objectives

- Build a real-time gesture recognition system.
- Detect human hands and faces using computer vision.
- Map gestures to meaningful application actions.
- Create interactive AR effects.
- Explore touchless human-computer interaction.
- Develop a modular and extensible computer-vision application.

---

## 🚀 Future Improvements

Possible future enhancements include:

- More gesture-controlled filters
- Custom gesture training
- Improved gesture accuracy
- Gesture-based application controls
- Voice + gesture hybrid interaction
- Multi-user gesture support
- More advanced 3D AR effects
- Mobile/web deployment
- Performance optimization
- Personalized AR filter creation

---

## 📚 Learning Outcomes

Through this project, I explored:

- Real-time computer vision
- Hand landmark detection
- Face landmark detection
- Gesture recognition
- Feature extraction
- Machine-learning concepts
- Image processing
- Augmented-reality rendering
- Modular Python application design
- Human-computer interaction

---

## 👩‍💻 Author

**Mehanaz Shaik**

B.Tech — Data Science

Interested in:

- Data Science
- Data Analytics
- Computer Vision
- Artificial Intelligence
- Software Development

### Connect

- LinkedIn: [Mehanaz Shaik](https://linkedin.com/in/mehanazshaik)
- GitHub: [mehanazshaik](https://github.com/mehanazshaik)

---

## ⭐ If You Like This Project

If you find GestureAR interesting, consider giving the repository a ⭐ on GitHub!