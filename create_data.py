import fiftyone as fo
import fiftyone.types.dataset_types
import fiftyone.zoo as foz
import fiftyone.utils.random as four
from ultralytics import YOLO
import fiftyone.utils.random as four

max_samples=1000
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


#classes_co=["person","car","bicycle","cat","dog"]
classes_oi= ["Person", "Car", "Bicycle", "Cat", "Monkey","Building","Man","Woman","Tree","Plant","Vehicle","Motorcycle","Bus","Chair"]
dataset=foz.load_zoo_dataset("open-images-v7", classes=classes_oi,max_samples=6000,label_types=['detections'])

"""
finetuning_data = fo.Dataset.from_dir(
    dataset_dir="custom_train",
    dataset_type=fo.types.YOLOv5Dataset,
    max_samples=max_samples,
    classes=classes_oi
)
finetuning_data = finetuning_data.map_labels(
    "ground_truth",
    {"Person":"person","Car":"car","Bicycle":"bicycle","Cat":"cat","Dog":"dog"}
)
four.random_split(
    finetuning_data,
    {"train": 0.8, "val": 0.2}
)"""
four.random_split(
    dataset,
    {"train": 0.66, "val": 0.34}
)
export_yolo_data(
    dataset,
    "data",
    classes_oi,
    split = ["train", "val"]
)
