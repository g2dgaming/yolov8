import fiftyone as fo
from ultralytics import YOLO
# The directory containing the dataset to import
dataset_dir = "yolo_predicted"

# The type of the dataset being imported


# Import the dataset
test_dataset = fo.Dataset.from_dir(
    dataset_dir= dataset_dir,
    dataset_type=fo.types.YOLOv5Dataset,
)
detection1_results = test_dataset.evaluate_detections(
    "prediction_original",
    eval_key="eval_original",
    compute_mAP=True,
    gt_field="ground_truth",
)

detection2_results = test_dataset.evaluate_detections(
    "prediction_fineTuned",
    eval_key="eval_fineTuned",
    compute_mAP=True,
    gt_field="ground_truth",
)
#sess

session=fo.launch_app(test_dataset)
session.wait()








