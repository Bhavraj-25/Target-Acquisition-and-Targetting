import cv2
import time
import torch
import serial

from torch.backends.mkl import verbose
from ultralytics import YOLO

device = "cuda" if torch.cuda.is_available() else "cpu"
print(f"Using device: {device}")

face_model = YOLO("models/yolov11l-face.pt").to(device)

SERIAL_PORT = "COM6"
BAUD_RATE = 9600

arduino = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
time.sleep(2)  # Wait for Arduino to initialize
print(f"Connected to Arduino on {SERIAL_PORT}")
# arduino = None

video_path = ""
video_cam = 0
FIXED_BBOX_WIDTH = 150
FIXED_BBOX_HEIGHT = 180

cap = cv2.VideoCapture(video_cam)
ret = True
while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.resize(frame, (640, 420))  # Resize for consistency
    results = face_model.predict(frame, conf=0.25, verbose = False)
    for result in results:
        boxes = result.boxes
        if boxes is not None:
            for box in boxes:
                # Get the center of the detected face
                x1, y1, x2, y2 = box.xyxy[0].cpu().numpy()
                center_x = int((x1 + x2) / 2)
                center_y = int((y1 + y2) / 2)

                # Calculate fixed bounding box coordinates centered on the face
                fixed_x1 = max(0, center_x - FIXED_BBOX_WIDTH // 2)
                fixed_y1 = max(0, center_y - FIXED_BBOX_HEIGHT // 2)
                fixed_x2 = min(frame.shape[1], center_x + FIXED_BBOX_WIDTH // 2)
                fixed_y2 = min(frame.shape[0], center_y + FIXED_BBOX_HEIGHT // 2)

                # Draw the fixed-size bounding box
                cv2.rectangle(frame, (fixed_x1, fixed_y1), (fixed_x2, fixed_y2), (0, 255, 0), 2)
                # Send x,y to arduino
                if arduino:
                    # Send center coordinates
                    coord_data = f"{center_x},{center_y}\n"
                    arduino.write(coord_data.encode())
                    print(f"Sent: {coord_data.strip()}")

                    # Try reading a response (non-blocking)
                    time.sleep(0.1)
                    if arduino.in_waiting:
                        response = arduino.readline().decode().strip()
                        print(f"Received: {response}")

                # Optional: Draw confidence score
                confidence = box.conf[0].cpu().numpy()
                cv2.putText(frame, f'{confidence:.2f}',
                            (fixed_x1, fixed_y1 - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
    cv2.imshow("Tracking", frame)

    # Break on 'q' key press
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
