import fiftyone as fo
from ultralytics import YOLO

# The directory containing the dataset to import
dataset_dir = "data"

# The type of the dataset being imported


# Import the dataset
dataset = fo.Dataset.from_dir(
    dataset_dir=dataset_dir,
    dataset_type=fo.types.YOLOv5Dataset,
    max_samples=500
)
model = YOLO("best.pt")

dataset.apply_model(model, label_field="prediction")

classes= ["Person", "Car", "Bicycle", "Cat", "Dog"]

detection_results = dataset.evaluate_detections(
    "prediction",
    eval_key="eval",
    compute_mAP=True,
    gt_field="ground_truth",
)
detection_results.print_report(classes=classes)