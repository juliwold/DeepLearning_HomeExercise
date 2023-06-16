import os
import glob

import geopandas as gpd

from find_paths import path_to_project
from process_predictions import clean_overlapping


def main():
    model_dir = os.path.join("..", "models")
    models = ["my_annotations_yolov8m.pt_640", "all_annotations_yolov8m.pt_640"]

    for model in models:
        project = os.path.join(path_to_project(model_dir, model))
        predicted_tiles = glob.glob(os.path.join(project, "predictions_processed", "*"))
        for tile in predicted_tiles:
            print(f"Processing predictions of {os.path.basename(tile)}.")
            out_dir = os.path.join(project, "predictions_IoU_th", os.path.basename(tile))
            os.makedirs(os.path.join(out_dir), exist_ok=True)
            predictions = gpd.read_file(os.path.join(tile, "predictions.shp"))
            cleaned_predictions = clean_overlapping(predictions)
            cleaned_predictions.to_file(os.path.join(out_dir, "predictions.shp"))


if __name__ == "__main__":
    main()
