# 🧮 Virtual Hand Gesture Calculator

This project is a **virtual calculator** controlled using **hand gestures** detected via a webcam. It leverages **OpenCV**, **cvzone**, and **mediapipe** for real-time hand tracking and gesture-based input.

## 🚀 Features

- Interactive on-screen calculator
- Operated using **pinch gestures** (index & middle finger)
- Supports:
  - Basic arithmetic operations (+, -, *, /)
  - Factorials (!)
  - Exponents (`pow`)
  - Backspace (←) and Clear (C)
- Visual feedback for hover and click
- Clean UI layout using OpenCV

## 🛠 Tech Stack

- Python
- OpenCV
- cvzone
- mediapipe

## 📸 How It Works

### 🖐️ Gesture Detection

- The system tracks **hand landmarks** using `cvzone.HandTrackingModule`.
- It specifically monitors the distance between the **index finger tip (id 8)** and the **middle finger tip (id 12)**.
- A **pinch gesture** (distance < 30) is treated as a "click".

### 🎛 Virtual Keyboard Setup

- Buttons are drawn using OpenCV `rectangle()` and `putText()`.
- The layout is a grid of `Button` objects defined in a 2D list (`keys`).
- Each button displays a mathematical operation or symbol.



