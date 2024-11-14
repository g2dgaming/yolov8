import cv2
import torch
import threading
import numpy as np
from ydlidar import YdLidarX4  # Replace with your model's actual class from the SDK

# Load YOLO model from PyTorch Hub
model = torch.hub.load('ultralytics/yolov5', 'yolov5s')  # Replace with your fine-tuned YOLO model

# Initialize the camera
cap = cv2.VideoCapture(0)  # Replace '0' with your camera ID

# Initialize LIDAR
lidar = YdLidarX4()  # Ensure this matches your YDLIDAR model class
lidar.set_lidar_options(port="/dev/ttyUSB0", baudrate=128000)  # Adjust port and baud rate as needed
lidar_data = []

def collect_lidar_data():
    global lidar_data
    lidar.connect()
    while True:
        # Get a new scan of 2D distance data points
        scan = lidar.get_scan()
        if scan:
            lidar_data = scan.points  # Update with the latest scan points

# Start LIDAR data collection in a separate thread
lidar_thread = threading.Thread(target=collect_lidar_data)
lidar_thread.daemon = True
lidar_thread.start()

# Helper function to get distance from LIDAR data at a specified (x, y) position
def get_lidar_distance(x, y, frame_width, frame_height):
    global lidar_data
    min_distance = None

    # Convert image (x, y) to LIDAR's angular range
    # Adjust as necessary for your coordinate system and alignment
    for point in lidar_data:
        angle_deg = np.degrees(point.angle)
        distance_m = point.distance

        # Simulate a mapping from LIDAR angle to image (x, y) coordinates if they are aligned
        angle_to_x = int((angle_deg / 360) * frame_width)
        if abs(angle_to_x - x) < 20:  # Narrow down by approximate horizontal position
            if min_distance is None or distance_m < min_distance:
                min_distance = distance_m

    return min_distance or 0  # Return 0 if no matching points found

while True:
    # Capture frame-by-frame from the camera
    ret, frame = cap.read()
    if not ret:
        break

    # YOLO object detection
    results = model(frame)
    detections = results.pandas().xyxy[0]  # Get results as a pandas dataframe

    # Loop through detections
    for index, row in detections.iterrows():
        x1, y1, x2, y2 = int(row['xmin']), int(row['ymin']), int(row['xmax']), int(row['ymax'])
        label = row['name']
        confidence = row['confidence']

        # Calculate object center for LIDAR overlay
        x_center, y_center = (x1 + x2) // 2, (y1 + y2) // 2

        # Retrieve distance data from LIDAR for each object center
        distance = get_lidar_distance(x_center, y_center, frame.shape[1], frame.shape[0])

        # Draw bounding box and label with distance
        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
        text = f"{label} {confidence:.2f} - {distance:.2f}m"
        cv2.putText(frame, text, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

        # Draw line from LIDAR position to the object center
        lidar_position = (50, 50)  # Adjust as necessary for your setup
        cv2.line(frame, lidar_position, (x_center, y_center), (255, 0, 0), 2)

    # Display the resulting frame
    cv2.imshow('YOLO with LIDAR Overlay', frame)

    # Press 'q' to break the loop
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Cleanup
cap.release()
lidar.disconnect()
cv2.destroyAllWindows()
