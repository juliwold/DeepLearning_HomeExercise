import os
import glob

from osgeo import gdal
import pandas as pd
import geopandas as gpd

from find_paths import path_to_project
import process_predictions


def main():
    gdal.UseExceptions()
    buffer_size = 1
    # ID of orthomosaics
    path_to_tiles = os.path.join("..", "data", "tiles", "test_data")
    tiles = glob.glob(os.path.join(path_to_tiles, "*"))

    # Define models to process predictions of.
    model_dir = os.path.join("..", "models")
    models = ["my_annotations_yolov8n.pt_256", "my_annotations_yolov8m.pt_640", "all_annotations_yolov8m.pt_640"]

    # Process predictions
    for model in models:
        print(f"Processing predictions for {model}.")
        project = path_to_project(model_dir, model)
        all_predictions = []
        for tile in tiles:
            ortho = os.path.basename(tile).strip("1234567890_")  # Remove tile prefix.
            print(f"Processing predictions of {ortho}.")
            out_dir = os.path.join(project, "predictions_processed", ortho)
            os.makedirs(os.path.join(out_dir), exist_ok=True)

            # Load tile index
            path_to_tile_index = glob.glob(os.path.join(tile, "*.shp"))[0]
            tile_index = gpd.read_file(path_to_tile_index)
            # Select predictions from tile.
            images = glob.glob(os.path.join(tile, "*.tif"))
            labels = glob.glob(
                os.path.join(project, "predict", "labels", f"{ortho}*.txt")
            )
            print(f"{len(images)} images detected.")
            print(f"{len(labels)} labels detected.")

            # Processing
            all_detections = []
            for i in images:
                # Find matching label.
                label = [
                    l
                    for l in labels
                    if str.strip(os.path.basename(i), ".tif")
                    in os.path.basename(l.strip(".txt"))
                ]
                if not label:
                    continue
                detections_tile = process_predictions.collect_bounding_boxes(
                    i, label[0], buffer_size, tile_index
                )
                all_detections.append(detections_tile)
            bounding_boxes = gpd.GeoDataFrame(
                pd.concat(all_detections, ignore_index=True)
            )
            # Clean up boxes with IoU threshold.
            cleaned_predictions = process_predictions.clean_overlapping(bounding_boxes, th = 0.7)
            all_predictions.append(cleaned_predictions)
            cleaned_predictions.to_file(
                os.path.join(out_dir, "predictions.shp"), driver="ESRI Shapefile"
            )
        predicted = gpd.GeoDataFrame(pd.concat(all_predictions, ignore_index=True))
        predicted.to_file(
            os.path.join(project, "processed_predictions", "predictions.shp")
        )


if __name__ == "__main__":
    main()
