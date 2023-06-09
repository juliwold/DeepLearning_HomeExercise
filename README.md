# Deep Learning - Home Exercise

Home exercise for NOVA course on deep learning in remote sensing.

[Models](<https://www.comet.com/juliwold/home-exercise-sapling-detector/view/uxR2erf0uJlERPXPjybwdN2yE/panels>)

## Objective

Compare the effect of training a seedling detector on your own annotated
dataset Vs full dataset (all annotations merged) on the detector’s performance.

## Data

### Train/Val data

- Own Annotations
  - Annotations made by me.
- Full annotations
  - Merging of all annotations made by students.

### Test data

- Tiled test data for evaluation using ML metrics. These data are located in
  /content/drive/MyDrive/NOVA_course_deep_learning/data/annotated_data/test
- Drone RGB orthomosaics for evaluation using domain metrics. The files are
  stored in
  /content/drive/MyDrive/NOVA_course_deep_learning/data/orthomosaics/test_data.
  Differently than the exercise done in class now, we will validate the
  detector’s performance in four sites where trees where the tree positions
  were measured with GPS in the field (reference trees are in
  /content/drive/MyDrive/NOVA_course_deep_learning/data/map_data/test_annotations2_sun.geojson).
  The field data were collected for four square plots (approx. 0.1 ha) per
  site.  

## Methods

### Stats

Provide stats on the number of annotated images and bounding boxes (some graph
would even be better). e.g

|          | Own data | Full data |
|----------|----------|-----------|
| n images |          |           |
| n trees  |          |           |

### Model Training

- Train a detector for each dataset and find the best (largest mAP@.5) set of
hyperparameters for model training such as model size (YOLOn, YOLOx,...),
image size (e.g. 640, 1000,...), …

### Model Evaluation

- Compare the evaluation metrics for the two detectors trained above (own and
  full) including:
  - ML (confusion matrices, mAP@.5, F1-curve).
  - Domain-specific (RMSE, bias, RMSE%, bias%, scatterplot of reference Vs
    predicted) on all of the four sites (in class we did only one site).

## Discussion

- Comment on the impact of different hyperparameters (model training) on the
  detectors’ performance and inference speed (some COMET plots would be greatly
  helpful to explain the experiment 😀).

- Is the model trained on more data better than the one trained on your own
  dataset? Discuss what could be the underlying causes.

- Provide at least three example screenshots of cases where the detector
  performed poorly and discuss what could be a good strategy to mitigate such
  issues.
