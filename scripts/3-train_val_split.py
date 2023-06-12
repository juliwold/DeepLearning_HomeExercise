import os
import shutil
import random


def main():
    path_to_annotated = os.path.join("..", "data", "annotated_data", "train")
    annotations = ["my_annotations"]

    # define split for training and validation
    split_train = 0.7

    for a in annotations:
        path_to_tiles = os.path.join(path_to_annotated, a, "annotated_tiles")
        output_dir = os.path.join(path_to_annotated, a)

        # Create directories to store data.
        for i in ["train", "val"]:
            for j in ["images", "labels"]:
                os.makedirs(os.path.join(output_dir, i, j), exist_ok=True)

        # List observations.
        tile_content = os.listdir(path_to_tiles)
        txt_files = [f for f in tile_content if f.endswith(".txt")]
        img_files = [f for f in tile_content if f.endswith(".tif")]

        # Select labels with images.
        txt_intersect = [
            f
            for f in txt_files
            if f.strip(".txt") in map(lambda x: x.strip(".tif"), img_files)
        ]
        print(f"{len(txt_intersect)} labels with image tiles.")

        train_size = round(0.7 * len(txt_intersect))
        print(f"{train_size} tiles drawn for training.")

        # Draw random sample.
        random.seed(3254)
        training_data = random.sample(txt_intersect, k=train_size)
        test_data = [f in training_data for f in txt_intersect]

        for i, label in enumerate(txt_intersect):
            if test_data[i]:
                dest_dir = os.path.join(output_dir, "train")
            else:
                dest_dir = os.path.join(output_dir, "val")
            # Move label
            src_label = os.path.join(path_to_tiles, label)
            shutil.copy(src_label, os.path.join(dest_dir, "labels", label))
            # Move image
            image = label.replace("txt", "tif")
            src_image = os.path.join(path_to_tiles, image)
            shutil.copy(src_image, os.path.join(dest_dir, "images", image))


if __name__ == "__main__":
    main()
