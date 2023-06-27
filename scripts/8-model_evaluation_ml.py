import os
import json

from ultralytics import YOLO

from find_paths import path_to_project, path_to_model


def main():
    model_dir = os.path.join("..", "models")
    models = [
        "my_annotations_yolov8n.pt_256",
        "my_annotations_yolov8n.pt_640",
        "all_annotations_yolov8m.pt_640",
    ]

    for model in models:
        project = os.path.join(path_to_project(model_dir, model))
        try:
            model_path = path_to_model(model_dir, model)
            yolo_model = YOLO(model_path)
        except FileNotFoundError:
            print("Model not found.")
            continue
        metrics = yolo_model.val(project=project, split="test")
        results = metrics.results_dict
        with open(os.path.join(project, "val", "test_results.json"), "w") as f:
            json.dump(results, f)


if __name__ == "__main__":
    main()
