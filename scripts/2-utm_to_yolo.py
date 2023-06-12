import os
import glob
import shutil

import geopandas as gpd
from PIL import Image

from yolo_conversions import utm_to_yolo


def main():
    annotations = ["my_annotations", "all_annotations"]
    path_to_tile_index = "..\\data\\map_data\\train_data_tile_index.geojson"
    tile_index = gpd.read_file(path_to_tile_index)

    class_ids = {"tree": 0}

    for a in annotations:
        print("--------")
        print(f"Processing {a}")
        path_to_tiles = os.path.join("..", "data", "tiles", a)
        path_to_annotation = os.path.join("..", "data", "annotated_data", "train", a)
        output_dir = os.path.join(path_to_annotation, "annotated_tiles")
        os.makedirs(output_dir, exist_ok=True)

        annotation = gpd.read_file(os.path.join(path_to_annotation, "annotations.shp"))
        annotation["class"] = "tree"

        tiles_imgs = glob.glob(os.path.join(path_to_tiles, "*.tif"))
        tiles_names = [os.path.basename(path) for path in tiles_imgs]
        tile_subset = tile_index[tile_index["ID"].isin(tiles_names)]

        # Iterate over tiles.
        for _, tile in tile_subset.iterrows():
            filename = tile["ID"]

            # Get tile polygon
            tile_poly = tile_index[tile_index["ID"] == filename]
            tile_bbox = tile["geometry"].bounds

            # Select annotations that intersect with tile.
            ann_in_tile = gpd.sjoin(
                annotation,
                tile_poly,
                how="inner",
                predicate="intersects",
            )

            # skip iteration if there are no annotations in a tile
            if len(ann_in_tile) == 0:
                print("No annotations.")
                continue

            # Check that image exists.
            if not os.path.exists(f"{path_to_tiles}\\{filename}"):
                print("skip")
                continue
            print("Annotations in tile.")

            # Load image.
            try:
                _ = Image.open(f"{path_to_tiles}\\{filename}")
            except:
                print("Unable to open image.")
                continue

            # Define the output file path
            output_file = os.path.join(
                output_dir, f"{os.path.splitext(filename)[0]}.txt"
            )

            # Convert annotations to YOLO and write to file.
            with open(output_file, "w") as f:
                yolo_annotations = utm_to_yolo(ann_in_tile, tile_bbox, class_ids)
                f.writelines(yolo_annotations)
            # Copy image to output.
            src_img = f"{path_to_tiles}\\{filename}"
            dest_img = f"{output_dir}\\{filename}"
            shutil.copy(src_img, dest_img)

if __name__ == "__main__":
    main()
