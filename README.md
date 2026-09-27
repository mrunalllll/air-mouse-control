# 🖱️ Air Mouse Control using OpenCV & MediaPipe

Control your computer mouse using hand gestures captured through a webcam. This project uses Computer Vision and Hand Tracking to move the cursor, perform clicks, scroll pages, and interact with the system without touching a physical mouse.

## 🚀 Features

* Move mouse cursor using index finger
* Left Click gesture
* Right Click gesture
* Drag and Drop support
* Smooth cursor movement
* Real-time hand tracking
* Webcam-based control
* Easy to use and beginner-friendly

## 🛠️ Technologies Used

* Python
* OpenCV
* MediaPipe
* PyAutoGUI
* NumPy

## 📂 Project Structure

```text
Air-Mouse-Control/
│
├── air_mouse.py
├── air_mouse_v2.py
├── requirements.txt
├── README.md
└── assets/
```

## 📦 Installation

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/air-mouse-control.git
cd air-mouse-control
```

### 2. Create Virtual Environment

```bash
python -m venv venv
```

### 3. Activate Virtual Environment

**Windows**

```bash
venv\Scripts\activate
```

### 4. Install Required Libraries

```bash
pip install opencv-python mediapipe pyautogui numpy
```

## ▶️ Run the Project

```bash
python air_mouse.py
```

or

```bash
python air_mouse_v2.py
```

## ✋ How It Works

1. Webcam captures live video.
2. MediaPipe detects hand landmarks.
3. Index finger position is tracked.
4. Finger movement is mapped to screen coordinates.
5. Mouse cursor moves according to hand movement.
6. Specific finger gestures trigger click actions.

## 📸 Hand Tracking

The project uses MediaPipe Hands which detects 21 hand landmarks in real time.

* Index Finger → Cursor Movement
* Pinch Gesture → Click
* Two-Finger Gesture → Additional Controls

## 📋 Requirements

* Python 3.10+
* Webcam
* Windows/Linux/MacOS

## 🎯 Applications

* Touchless Computer Control
* Accessibility Assistance
* Smart Presentations
* Gesture-Based Human Computer Interaction
* Computer Vision Learning Project

## 🔮 Future Improvements

* Volume Control
* Brightness Control
* Gesture-Based Media Control
* Multi-Hand Support
* AI-Powered Gesture Recognition

## 🤝 Contributing

Contributions are welcome. Feel free to fork this repository and submit pull requests.

## 📜 License

This project is open-source and available under the MIT License.

## 👨‍💻 Author

**Mrunal Kiran Bhimarapu**

First-Year Computer Science Engineering Student
Sandip University, Nashik

Passionate about AI, Machine Learning, Computer Vision, and Software Development.

⭐ If you like this project, don't forget to star the repository!
