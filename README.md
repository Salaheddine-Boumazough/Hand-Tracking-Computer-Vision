# Real-Time Hand Tracking and Computer Vision Applications

## Description
This repository features a robust, class-based Hand Tracking Module built on top of Google's MediaPipe framework and OpenCV. The project demonstrates how to extract 21 hand landmarks in real-time to create interactive applications, including gesture-based volume control and a Rock-Paper-Scissors game.

## Key Features
- HandTrackingModule: A reusable Python class that handles hand detection, landmark positioning, and handedness (Left/Right) classification.
- Volume Controller: Adjust system master volume using the distance between the thumb and index finger.
- Rock Paper Scissors: A fully functional game with a countdown system and automated win-tracking logic.
- Finger Counter: A real-time counting system that utilizes landmark geometry to detect extended fingers.

## Technical Stack
- Python 3.x
- OpenCV (Computer Vision)
- MediaPipe (Hand Tracking Inference)
- NumPy (Data Transformation)
- Pycaw (System Audio Control)

## Installation

1. Clone the repository:
   git clone https://github.com/YourUsername/Hand-Tracking-CV.git

2. Install the required dependencies:
   pip install -r requirements.txt

## Usage

### Using the Module
To use the tracker in your own project, import the HandTrackingModule:

from HandTrackingModule import handDetector
detector = handDetector()

### Running Applications
To run the Rock-Paper-Scissors game:
python rock_paper_scissor.py

To run the Volume Controller:
python volume.py

## Project Structure
- HandTrackingModule.py: The core detection logic.
- rock_paper_scissor.py: Game logic and state management.
- volume.py: Mapping hand distance to system audio levels.
- fingerCounter.py: Hand gesture recognition for counting.

## License
Distributed under the MIT License. See LICENSE for more information.
