import os
import yaml

import pandas as pd
from itertools import product
import comet_ml

comet_ml.init(project_name='seedling_detection_YOLOv8')

import ultralytics

ultralytics.checks()

path_to_annotated = "..\\data\\annotated_data\\train"
annotations = ("my_annotations", "all_annotations")

data_configs = []
for a in annotations:
    path_to_tiles = f"{path_to_annotated}\\{a}"
    config_data = {
        'path': os.path.abspath(path_to_tiles),
        'train': os.path.abspath(f"{path_to_tiles}\\train\\images"),
        'val': os.path.abspath(f"{path_to_tiles}\\val\\images"),
        'test':os.path.abspath("..\\data\\annotated_data\\test\\images"), # this is by default
        'names': {
            0: 'tree'
        }
    }
    config = f"{path_to_tiles}\\train_config.yaml"
    data_configs.append(config)
    with open(config, "w") as file:
        yaml.dump(config_data, file)

hyperamaters = {
    "data": data_configs,
    "model": ["yolov8n.pt", "yolov8s.pt", "yolov8m.pt", "yolov8l.pt", "yolov8x.pt"],
    "img_size": [250, 500, 1000, 2000],
}
model_settings = pd.DataFrame(
    [row for row in product(*hyperamaters.values())],
    columns=hyperamaters.keys()
)

model_settings["annotations"] = model_settings["data"].str.extract("(my_annotations|all_annotations)")
model_settings["project"] =  "models\\" + model_settings["annotations"]
model_settings["name"] = (
    model_settings["annotations"] + "_" +
    model_settings["model"] + "_" +
    model_settings["img_size"].astype(str)
)

# Test run
hyperamater_settings = model_settings.iloc[0, :]

model = ultralytics.YOLO(hyperamater_settings["model"])

model.train(
    data = hyperamater_settings["data"],
    epochs = 3,
    imgsz = int(hyperamater_settings["img_size"]),
    name = "test_run",
    project = ".test_runs"
)

for i, settings in model_settings.iterrows():
    model = ultralytics.YOLO(settings["model"])
    model.train(
        data = settings["data"],
        epochs = 350,
        imgsz = int(settings["img_size"]),
        name = settings["name"],
        project = settings["project"]
    )
