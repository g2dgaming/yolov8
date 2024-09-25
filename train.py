
if __name__ == '__main__':
    import torch

    device = torch.device("cuda:0")
    x = torch.ones(1, device=device)
    print("GPU Available: ", torch.cuda.is_available())
    print(x)
    from ultralytics import YOLO

    # Load a model
    model = YOLO('runs/detect/train9/weights/best.pt')  # load a pretrained model (recommended for training)

    # Train the model with 2 GPUs
    results = model.train(data='yolov9_train/dataset.yaml', epochs=50, imgsz=640, device='cuda:0')