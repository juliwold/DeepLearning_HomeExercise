# Home excericse - NOVA course on deep learning in remote sensing
Julius Wold

# Introduction

## Objective

Compare the effect of training a seedling detector on your own annotated
dataset vs. the full dataset on the detector’s performance.

# Materials and methods

## Annotations

Two sets of annotations were used for model tranining: “My annotations”
and “All annotations”.

- “My annotations”
  - Annotations made by the author.
- “All annotations”
  - Annotations from all students merged.

<div id="tbl-training">

| All annotations | My annotations |
|----------------:|---------------:|
|             271 |             34 |
|             116 |             14 |
|             387 |             48 |
|            3492 |            201 |
|            1570 |             79 |
|            5062 |            280 |

Table 1: Training data

</div>

## Model training

YOLOv8 models were trained using the dataset “My annotations” and the
dataset “All annotations”. A grid search were performed for model sizes
“Nano”, “Medium” and “Xtra large” and image sizes 256, 640 and 1024. The
best mode for each dataset were selected using mAP@.5.

<div id="tbl-search">

| Model      | Image size |
|:-----------|-----------:|
| yolov8n.pt |        256 |
| yolov8n.pt |        640 |
| yolov8n.pt |       1024 |
| yolov8m.pt |        256 |
| yolov8m.pt |        640 |
| yolov8m.pt |       1024 |
| yolov8x.pt |        256 |
| yolov8x.pt |        640 |
| yolov8x.pt |       1024 |

Table 2: Grid search.

</div>

## Model evaluation

The selected models from the model training were evaluated using
machine-learning metris and domain metrics.

### ML metrics

Machine learning metrics were evaluated by testing the models against
tiled test data.

## Domain metrics

$$
RMSE = \sqrt{\frac{\Sigma_{i=1}^{n}(y_i - \hat{y_i})^2}{n}}
$$

$$
MD = \frac{\Sigma_{i=1}^{n}(y_i - \hat{y_i})}{n}
$$

# Results & Discussion

## Model training

Models trained by the “My annotation” dataset achived better performance
in training than the models trained on “All annotations”. For “My
annotation” the highest performance was acchived by the YOLOv8 nano
model with image size 256 (mAP@.5 of 061 at epoch 133).

``` r
my_perfomance <-
    here("models", "model_performance", "juliwold_home_exercise_sapling_detector_sapling_detector_table_data_my_annotations.csv") %>%
    read_csv(show_col_types = FALSE) %>%
    select(-data)
all_perfomance <-
    here("models", "model_performance", "juliwold_home_exercise_sapling_detector_sapling_detector_table_data_all_annotations.csv") %>%
    read_csv(show_col_types = FALSE) %>%
    select(-data)
```

``` r
knitr::kable(my_perfomance)
```

<div id="tbl-trainingperformance-1">

| Name                        | model      | imgsz | metrics/mAP50(B) | metrics/mAP50-95(B) | metrics/precision(B) | metrics/recall(B) | model/speed_PyTorch(ms) |
|:----------------------------|:-----------|------:|-----------------:|--------------------:|---------------------:|------------------:|------------------------:|
| large_jay_4099              | yolov8x.pt |  1024 |        0.5446111 |           0.2283048 |            0.5513068 |         0.5443038 |                  24.577 |
| territorial_neutrino_6707   | yolov8x.pt |   640 |        0.5109202 |           0.2346482 |            0.6636091 |         0.4556962 |                  10.645 |
| advanced_magpie_8288        | yolov8x.pt |   256 |        0.5358150 |           0.2107009 |            0.5508817 |         0.5745127 |                   6.930 |
| scarlet_junglefowl_7165     | yolov8m.pt |  1024 |        0.5420742 |           0.2688545 |            0.5947237 |         0.5443038 |                   9.502 |
| key_pig_4200                | yolov8m.pt |   640 |        0.5643102 |           0.2563338 |            0.5351010 |         0.6556569 |                   6.573 |
| responsible_salamander_2800 | yolov8m.pt |   256 |        0.5590641 |           0.2463685 |            0.5988782 |         0.6708861 |                   7.859 |
| given_stem_7294             | yolov8n.pt |  1024 |        0.5194810 |           0.2278253 |            0.6920768 |         0.4552118 |                   4.001 |
| super_runoff_1234           | yolov8n.pt |   640 |        0.5929308 |           0.2810344 |            0.6016476 |         0.6691550 |                   4.287 |
| petite_honeydew_9364        | yolov8n.pt |   256 |        0.5527550 |           0.2516653 |            0.5899404 |         0.5696203 |                   4.787 |

Table 3: My annotations

</div>

``` r
knitr::kable(all_perfomance)
```

<div id="tbl-trainingperformance-2">

| Name                          | model      | imgsz | metrics/mAP50(B) | metrics/mAP50-95(B) | metrics/precision(B) | metrics/recall(B) | model/speed_PyTorch(ms) |
|:------------------------------|:-----------|------:|-----------------:|--------------------:|---------------------:|------------------:|------------------------:|
| nosy_muskox_8487              | yolov8x.pt |  1024 |        0.3254724 |           0.1150182 |            0.3878833 |         0.4484076 |                  25.644 |
| purple_caramel_8526           | yolov8x.pt |   640 |        0.3236185 |           0.1206460 |            0.4255610 |         0.4471338 |                  10.408 |
| wild_wine_2139                | yolov8x.pt |   256 |        0.3164349 |           0.1110326 |            0.4033215 |         0.4684254 |                   2.897 |
| implicit_rooster_8021         | yolov8m.pt |  1024 |        0.3278949 |           0.1263731 |            0.4130336 |         0.4598726 |                   9.942 |
| aggressive_cephalopod_26      | yolov8m.pt |   640 |        0.3641667 |           0.1293037 |            0.3932170 |         0.5261146 |                   4.113 |
| relative_urial_234            | yolov8m.pt |   256 |        0.3356432 |           0.1107747 |            0.3755790 |         0.4445860 |                   2.009 |
| forward_factory_2576          | yolov8n.pt |  1024 |        0.3259859 |           0.1219144 |            0.4184633 |         0.4114650 |                   2.320 |
| smiling_cottage_5709          | yolov8n.pt |   640 |        0.3419662 |           0.1237630 |            0.4081213 |         0.4662420 |                   1.595 |
| extraordinary_rattlesnake_589 | yolov8n.pt |   256 |        0.3248398 |           0.1140287 |            0.3835007 |         0.4624204 |                   1.216 |

Table 4: All annotations

</div>

Training performance of best model.

> Detailed view of trained models can be found in [this Comet
> project](https://www.comet.com/juliwold/home-exercise-sapling-detector/view/uxR2erf0uJlERPXPjybwdN2yE/panels).

    `geom_smooth()` using method = 'loess' and formula = 'y ~ x'

<img src="report_files/figure-commonmark/fig-training-1.png"
id="fig-training" alt="Figure 1: Training results" />

## Model evaluation

### ML metrics

<div id="tbl-mlmetrics">

|                                | metrics/precision(B) | metrics/recall(B) | metrics/mAP50(B) | metrics/mAP50-95(B) | fitness |
|:-------------------------------|---------------------:|------------------:|-----------------:|--------------------:|--------:|
| all_annotations_yolov8m.pt_640 |                 0.56 |              0.45 |             0.38 |                0.12 |    0.14 |
| my_annotations_yolov8n.pt_256  |                 0.48 |              0.33 |             0.28 |                0.08 |    0.10 |
| my_annotations_yolov8n.pt_640  |                 0.49 |              0.42 |             0.36 |                0.11 |    0.14 |

Table 5: Machine learnining metrics.

</div>

### Domain

<div id="tbl-comainmetrics">

| RMSE | RMSE (%) |   MD | MD (%) |
|-----:|---------:|-----:|-------:|
|  981 |       67 |  891 |     61 |
|  692 |       34 |  662 |     33 |
|   99 |        9 |   90 |      8 |
|  386 |       29 |  353 |     27 |
|  632 |       43 |  499 |     34 |
| 1363 |       93 | 1307 |     89 |
| 1360 |       67 | 1331 |     66 |
|  471 |       43 |  465 |     43 |
|  691 |       52 |  684 |     52 |
| 1049 |       71 |  947 |     64 |
| 1436 |       98 | 1368 |     94 |
| 1613 |       80 | 1574 |     78 |
|  761 |       70 |  759 |     70 |
| 1063 |       81 | 1054 |     80 |
| 1262 |       86 | 1188 |     81 |

Table 6: Domain metrics.

</div>

# Conclusion
