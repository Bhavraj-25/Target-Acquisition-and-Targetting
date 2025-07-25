# Target-Acquisition-and-Targeting 

A conceptual prototype of a Sniper Advanced Targeting Pod using a standard camera, Arduino, and servo-driven gimbal for real-time object tracking and directional estimation.

## Overview

This project simulates a simplified version of a military-grade targeting pod system. It utilizes a standard USB/web camera for object detection and an Arduino-controlled gimbal mechanism to track and orient toward the target. The direction is estimated using a clock-based reference (e.g., “3 o’clock”) by dividing the field of view into sectors. The system uses serial communication to interface between the PC (running the tracking algorithm) and the Arduino (driving the servo motors).

## Features

-  Real-time video feed from a standard camera  
-  Object tracking using computer vision (OpenCV)  
-  Direction estimation in 12-clock format (e.g., “Target at 5 o’clock”)  
-  2-axis servo-based gimbal mount for automatic target alignment  
-  Arduino–PC serial communication for real-time commands  
-  3D-printed modular enclosure and lightweight structure  

## System Architecture
<img width="1224" height="896" alt="flowchart" src="https://github.com/user-attachments/assets/1bd04bde-7c9c-46ee-af28-ee4d525bb651" />

## Technologies Used

- Arduino UNO  
- Python (OpenCV, PySerial)  
- Servo Motors 
- USB/Web Camera  
- 3D Printed Components  
- Serial Communication  

## How It Works

1. The PC captures live frames from a standard webcam.  
2. Python processes the frames using basic object detection techniques (e.g., color thresholding, contours, or motion).  
3. The target's position is computed by analyzing its relative displacement in (x, y) coordinates from the system's origin and is assigned to a directional sector for tactical orientation and engagement planning. 
4. A serial command is sent to Arduino indicating the required adjustment.  
5. The Arduino adjusts the gimbal's X and Y angles using servo motors to align with the target.  

## Getting Started

1. Clone the repository:

   ```bash
   git clone https://github.com/Bhavraj-25/Target-Acquisition-and-Targetting.git  
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
- Integration with the Raspberry Pi will allow it to manage object detection, tracking, and hardware control in a unified system. 
- Implement multi-target prioritization logic  

## Developed By
Bhavraj Sairem  
🖂sairem.bhavraj2512@gmail.com 🔗https://github.com/Bhavraj-25 🌐https://www.linkedin.com/in/bhavraj-sairem-450253293  

## Contributors
Divanshu  
🖂divanshu0213@gmail.com  🔗https://github.com/dvanhu 🌐https://www.linkedin.com/in/dvanhu/
