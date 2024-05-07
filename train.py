import torch
if torch.backends.mps.is_available():
    mps_device = torch.device("mps")
    x = torch.ones(1, device=mps_device)
    print (x)
else:
    print ("MPS device not found.")

from ultralytics import YOLO

# Load a model
model = YOLO('yolov8l-oiv7.pt')  # load a pretrained model (recommended for training)

# Train the model with 2 GPUs
results = model.train(data='data/dataset.yaml', epochs=30, imgsz=640, device='mps')