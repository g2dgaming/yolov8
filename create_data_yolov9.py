import fiftyone as fo
import fiftyone.types
import fiftyone.utils.random as four
from ultralytics import YOLO
dataset_dir = "data"
#Open Images Filter classes

classes_oi= ["person", "car", "bicycle", "cat", "monkey","building","man","woman","tree","plant","vehicle","motorcycle","bus","chair"]
#train_dataset = fo.Dataset.from_dir(
#    dataset_dir,fiftyone.types.YOLOv5Dataset)


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
"""
train_dataset=train_dataset.map_labels("ground_truth", {"Person": "person", "Car": "car", "Bicycle": "bicycle", "Cat": "cat", "Building": "building","Man":"man", "Monkey":"monkey","Woman":"woman","Tree":"tree","Plant": "plant","Vehicle":"vehicle","Motorcycle":"motorcycle","Bus":"bus", "Chair":"chair"})
train_dataset.untag_samples(train_dataset.distinct("tags"))
four.random_split(
    train_dataset,
    {"train": 0.34, "val": 0.66}
)

export_yolo_data(
    train_dataset,
    "yolov9_train",
    classes_oi,
    split=["train", "val"]

)"""
val_dataset = fo.Dataset.from_dir(
    dataset_dir,fiftyone.types.YOLOv5Dataset,split="val",max_samples=1000)

val_dataset=val_dataset.map_labels("ground_truth", {"Person": "person", "Car": "car", "Bicycle": "bicycle", "Cat": "cat", "Building": "building","Man":"man", "Monkey":"monkey","Woman":"woman","Tree":"tree","Plant": "plant","Vehicle":"vehicle","Motorcycle":"motorcycle","Bus":"bus", "Chair":"chair"})
val_dataset.untag_samples(val_dataset.distinct("tags"))



export_yolo_data(
    val_dataset,
    "yolov9_val",
    classes_oi,
    split = "val"
)