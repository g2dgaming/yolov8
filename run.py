import cv2
import torch
from ultralytics import YOLO

# Load your YOLO model (replace 'bnest.pt' with the correct path to your model)
model = YOLO('yolov8n-oiv7.pt')

# Open a connection to your webcam
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Error: Could not open video stream from webcam.")
    exit()

# Process webcam stream in real-time
while True:
    # Capture frame-by-frame from the webcam
    ret, frame = cap.read()
    if not ret:
        print("Failed to grab frame")
        break

    # YOLO model inference on the frame
    results = model(frame)

    # Draw bounding boxes and labels on the frame
    annotated_frame = results[0].plot()  # Plot the bounding boxes on the frame

    # Display the resulting frame
    cv2.imshow('YOLOv5 Real-time Detection', annotated_frame)

    # Break the loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything is done, release the capture and close windows
cap.release()
cv2.destroyAllWindows()
