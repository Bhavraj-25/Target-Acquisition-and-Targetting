import cv2
import time
import torch
import serial
import numpy as np

from torch.backends.mkl import verbose
from ultralytics import YOLO

# To switch to gpu
device = "cuda" if torch.cuda.is_available() else "cpu"
print(f"Using device: {device}")

# Serial com port
SERIAL_PORT = "COM6"
BAUD_RATE = 9600

# Initialize arduino connection
arduino = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
time.sleep(2)
print(f"Connected to Arduino on {SERIAL_PORT}")

# Load model
model = YOLO("models/best.pt").to(device)

# Video path or video cam
video_path = "test_videos/trial.mp4q"
video_cam = 0

# Initialize tracking variables
tracker = None
tracking = False
track_window = None
frame = None
mouse_x, mouse_y = 240, 240  # Default cursor position

# Fixed cursor and square properties
cursor_height = 22  # Fixed cursor height
cursor_spacing = 15  # Space between the two vertical lines
square_size = 40  # Fixed tracking square size

# def preprocess_frame(frame):
#     """Prepares the frame for YOLO tracking by converting it to a tensor."""
#     frame_tensor = torch.from_numpy(frame).permute(2, 0, 1).unsqueeze(0).float()  # Convert to BCHW
#     frame_tensor = frame_tensor / 255.0  # Normalize to [0,1]
#     return frame_tensor.to(device)

def mouse_callback(event, x, y, flags, param):
    """Handles both mouse movement and object selection."""
    global mouse_x, mouse_y, tracking, track_window, tracker, frame

    mouse_x, mouse_y = x, y  # Update cursor position

    if event == cv2.EVENT_LBUTTONDOWN:
        if frame is None:
            return

        if not isinstance(frame, (torch.Tensor, np.ndarray)):
            print("Error: Frame is not a valid NumPy array")
            return

        # Centered tracking box of fixed size
        x1, y1 = max(0, x - square_size // 2), max(0, y - square_size // 2)
        x2, y2 = x1 + square_size, y1 + square_size
        track_window = (x1, y1, x2, y2)

        #frame_tensor = preprocess_frame(frame)
        res = model.track(frame, persist=True, verbose=False)

        if res and hasattr(res[0], 'boxes') and len(res[0].boxes) > 0:
            for box in res[0].boxes.xyxy:
                x_min, y_min, x_max, y_max = map(int,box.tolist())
                if x_min <= x <= x_max and y_min <= y <= y_max:
                    tracking = True
                    track_window = (x_min, y_min, x_max, y_max)
                    break

    if event == cv2.EVENT_RBUTTONDOWN:
        tracking = False
        print("tracking stopped.")


# Set up OpenCV window and mouse callback
cv2.namedWindow("Tracking")
cv2.setMouseCallback("Tracking", mouse_callback)

cap = cv2.VideoCapture(video_path)
ret = True
while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.resize(frame, (640, 420))  # Resize for consistency

    if tracking and track_window:
        #frame_tensor = preprocess_frame(frame)
        # res = model.predict(frame, conf=0.5, verbose=False)
        res = model.track(frame, conf=0.5, persist=True ,verbose=False)

        success = res and hasattr(res[0], 'boxes') and len(res[0].boxes) > 0

        if success:
            for box in res[0].boxes.xyxy:
                x_min, y_min, x_max, y_max = map(int, box.tolist())  # Convert to integers - (contains coordinates of bounding box)
                centre_x, centre_y = (x_min + x_max)//2, (y_min + y_max)//2  # Centre coordinates of bounding box
                small_width, small_height = 80, 55  # Dimensions of small rectangle

                # Fixed rectangle coordinates
                small_x1 = centre_x - small_width//4
                small_y1 = centre_y - small_height//4
                small_x2 = centre_x + small_width//4
                small_y2 = centre_y + small_height//4
                cv2.rectangle(frame, (small_x1, small_y1), (small_x2, small_y2), (0, 255, 0), 2)

                if arduino:
                    # Send center coordinates
                    coord_data = f"{centre_x},{centre_y}\n"
                    arduino.write(coord_data.encode())
                    print(f"Sent: {coord_data.strip()}")

                    # Try reading a response (non-blocking)
                    time.sleep(0.1)
                    if arduino.in_waiting:
                        response = arduino.readline().decode().strip()
                        print(f"Received: {response}")

        else:
            # print("Tracking lost!")
            tracking = False

    # Line for TDC cursor
    cv2.line(frame, (mouse_x - cursor_spacing, mouse_y - cursor_height // 2),
             (mouse_x - cursor_spacing, mouse_y + cursor_height // 2), (0, 255, 0), 3)
    cv2.line(frame, (mouse_x + cursor_spacing, mouse_y - cursor_height // 2),
             (mouse_x + cursor_spacing, mouse_y + cursor_height // 2), (0, 255, 0), 3)

    # Display the video
    cv2.imshow("Tracking", frame)

    # Break on 'q' key press
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
