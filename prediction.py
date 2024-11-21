import fiftyone as fo
import fiftyone.types.dataset_types
import fiftyone.zoo as foz
import fiftyone.utils.random as four
from ultralytics import YOLO
import fiftyone.utils.random as four
max_samples=30
classes_oi= ["Person", "Car", "Bicycle", "Cat", "Dog"]

dataset = fo.Dataset.from_dir(
    dataset_dir="custom_train",
    dataset_type=fo.types.YOLOv5Dataset,
    max_samples=max_samples,
    classes=classes_oi
)
model=YOLO("best.pt")
dataset.apply_model(model,label_type="prediction")

session = fo.launch_app(dataset)
session.wait()