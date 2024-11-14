import cv2
from ultralytics import YOLO

model = YOLO('yolov8n-oiv7.pt')
class_ids = [96, 160, 381, 393, 567]
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Error: Could not open video stream from webcam.")
    exit()
while True:
    ret, frame = cap.read()
    if not ret:
        print("Failed to grab frame")
        break
    results = model.predict(source=frame)
    predicted_frame = results[0].plot()
    cv2.imshow('YOLOv8 Real-time Detection', predicted_frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()

