# Target-Acquisition-and-Targetting 

A conceptual prototype of a Sniper Advanced Targeting Pod using a standard camera, Arduino, and servo-driven gimbal for real-time object tracking and directional estimation.

## Overview

This project simulates a simplified version of a military-grade targeting pod system. It utilizes a standard USB/web camera for object detection and an Arduino-controlled gimbal mechanism to track and orient toward the target. The direction is estimated using a clock-based reference (e.g., “3 o’clock”) by dividing the field of view into sectors. The system uses serial communication to interface between the PC (running the tracking algorithm) and the Arduino (driving the servo motors).

Built as a final-year B.Tech project, it demonstrates the feasibility of low-cost, modular, and scalable defense-inspired systems using accessible hardware and software tools.

## Features

-  Real-time video feed from a standard camera  
-  Object tracking using computer vision (OpenCV)  
-  Direction estimation in 12-clock format (e.g., “Target at 5 o’clock”)  
-  2-axis servo-based gimbal mount for automatic target alignment  
-  Arduino–PC serial communication for real-time commands  
-  3D-printed modular enclosure and lightweight structure  

## System Architecture

## Technologies Used

- Arduino UNO  
- Python (OpenCV, PySerial)  
- Servo Motors (SG90 / MG90S)  
- USB/Web Camera  
- 3D Printed Components  
- Serial Communication  

## How It Works

1. The PC captures live frames from a standard webcam.  
2. Python processes the frames using basic object detection techniques (e.g., color thresholding, contours, or motion).  
3. The target’s location is mapped to one of 12 directional sectors (clock system).  
4. A serial command is sent to Arduino indicating the required adjustment.  
5. The Arduino adjusts the gimbal's X and Y angles using servo motors to align with the target.  

## Getting Started

1. Clone the repository:

   ```bash
   git clone https://github.com/dvanhu/Target-Acquisition-and-Targetting.git  
Upload the Arduino sketch from the /arduino/ directory to your Arduino UNO using the Arduino IDE.

Run the Python script from the /python/ directory:

 ``` python tracker.py ```
Connect the Arduino to your PC using a USB cable.
Tune object detection parameters as needed (color range, contour area, etc.).

## Project Structure
 ```
/arduino/      → Arduino code for servo control via serial  
/python/       → Python code for video capture, object tracking, and serial commands  
/media/        → Screenshots, demo images, or videos (optional)  
README.md      → Project documentation
 ```
## Demo 
https://github.com/user-attachments/assets/03807d78-b897-4e23-a0d6-2b5f19f0f924

## 3D Model Preview  
https://github.com/Bhavraj-25/Target-Acquisition-and-Targetting/blob/29f0abaec44d27b8148fe7d45c085e3a889ac96e/3D%20Model/pod_track%20v3.stl


## Future Enhancements

- Add support for AI-based object detection (YOLO, Haar cascades)  
- Replace USB camera with thermal or night-vision camera  
- Integrate with ESP32 for wireless control  
- Add GUI dashboard using PyQt or Streamlit  
- Implement multi-target prioritization logic  

## Developed By
Bhavraj Sairem  
🖂sairem.bhavraj2512@gmail.com 🔗https://github.com/Bhavraj-25 🌐https://www.linkedin.com/in/bhavraj-sairem-450253293  

## Contributors
Divanshu  
🖂divanshu0213@gmail.com  🔗https://github.com/dvanhu 🌐https://www.linkedin.com/in/dvanhu/
