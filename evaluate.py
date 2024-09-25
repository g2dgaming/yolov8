import fiftyone as fo
import fiftyone.types
from ultralytics import YOLO

# The directory containing the dataset to import
dataset_dir = "yolov9_test"
#Open Images Filter classes
classes_oi= ["person", "car", "bicycle", "cat", "monkey","building","man","woman","tree","plant","vehicle","motorcycle","bus","chair"]

# The type of the dataset being imported


# Import the dataset
test_dataset = fo.Dataset.from_dir(
    dataset_dir,fiftyone.types.YOLOv5Dataset,max_samples=1000)

original_model = YOLO("yolov8s.pt")
fineTuned_model = YOLO("fineTuned.pt")


test_dataset.apply_model(original_model, label_field="prediction_original")
test_dataset.apply_model(fineTuned_model, label_field="prediction_fineTuned")

def export_yolo_data(
    samples,
    export_dir,
    classes,
    label_field = "ground_truth",
    split = None
    ):

    if type(split) == list:
        splits = split
        for split in splits:
            export_yolo_data(
                samples,
                export_dir,
                classes,
                label_field,
                split
            )
    else:
        if split is None:
            split_view = samples
            split = "val"
        else:
            split_view = samples.match_tags(split)
        split_view.export(
            export_dir=export_dir,
            dataset_type=fo.types.YOLOv5Dataset,
            label_field=label_field,
            classes=classes,
            split=split
        )

export_yolo_data(
    test_dataset,
    "yolo_predicted",
    classes_oi
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
session=fo.launch_app(test_dataset)
session.wait()
#detection1_results.print_report(classes=classes_oi)
#detection2_results.print_report(classes=classes_oi)



