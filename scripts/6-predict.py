import os
import glob

from ultralytics import YOLO


def path_to_project(model_dir, model_name):
    if "my_annotations" in model_name:
        sub_dir = "my_annotations"
    else:
        sub_dir = "all_annotations"
    project = os.path.join(model_dir, sub_dir, model_name)

    return(project)


def path_to_model(model_dir, model_name):
    model_path = os.path.join(path_to_project(model_dir, model_name), "weights", "best.pt")

    return model_path


def main():
    #
    path_to_tiles = os.path.join("..", "data", "tiles", "test_data")
    tiles = glob.glob(os.path.join(path_to_tiles, "*"))
    # Define models to predict with.
    model_dir = os.path.join("..", "models")
    models = [
        {"name": "my_annotations_yolov8m.pt_640", "conf": 0.60},
        {"name": "all_annotations_yolov8m.pt_640", "conf": 0.23},
    ]

    for model in models:
        # Load model.
        project = path_to_project(model_dir, model["name"])
        try:
            model_path = path_to_model(model_dir, model["name"])
            yolo_model = YOLO(model_path)
        except FileNotFoundError:
            print("Model not found.")
            continue
        print(f"\n\nPredicting using {model['name']}.")

        # Make predictions.
        for tile in tiles:
            print(f"Predicting for {os.path.basename(tile)}.")
            yolo_model.predict(
                source=tile,
                project=project,
                conf=model["conf"],
                save=True,
                save_txt=True,
                save_conf=True,
                line_width=1,
            )

if __name__ == "__main__":
    main()
