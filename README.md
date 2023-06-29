# Deep Learning - Home Exercise

Home exercise for NOVA course on deep learning in remote sensing.

Models trained for this exercise can be found in this [Comet project](<https://www.comet.com/juliwold/home-exercise-sapling-detector/view/uxR2erf0uJlERPXPjybwdN2yE/panels>).

## Overview

The repository consists four folders:

- figures
  - Contains Comet figures used in report.
- models
  - Contains results from training for all models.
    - Weights of models are not included (*best.pt* can be collected from Comet).
  - Selected models contains processed predictions and evaluation metrics.
- report
  - Contains report and the *qmd* file generating the report.
- scripts
  - Contains scripts used in the experiments

## Scripts

### Main scripts

- 1-tile_train_data.py
  - Tiles data to annotate and use in training. Unused as data was already tiled and annotated.
- 2-utm_to_yolo.py
  - Converts annotations from geospatial format to yolo format.
- 3-train_val_split.py
  - Performs train/val split on data.
- 4-model_training.py
  - Trains the YOLO models using a grid search.
- 5-tile-test-data.py
  - Tile the test data for predicting on.
- 6-model_inferrence.py
  - Perform predictions on tiled test data.
- 7-post_process_predictions.py
  - Convert the predictions from yolo to geospatial format.
  - Apply Intersect over Union (IoU) filter.
- 8-model_evaluation_ml.py
  - Evaluate model using ml metrics.
- 9-model_evaluation_domain.py
  - Evaluate models using domain metrics.

### Helper scripts

- find_paths.py
  - Helper functions to find project and model paths.
- process_predictions.py
  - Functions to collect bounding boxes from tiles and apply IoU filter.
- tile_data.py
  - Function for tiling orthomosaics.
- yolo_conversions.py
  - Functions for converting between yolo and geospatial formats.
