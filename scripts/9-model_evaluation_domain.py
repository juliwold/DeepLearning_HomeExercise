import os

import numpy as np
import pandas as pd
import geopandas as gpd

from find_paths import path_to_project

def main():
    model_dir = os.path.join("..", "models")
    models = ["my_annotations_yolov8n.pt_256", "my_annotations_yolov8m.pt_640", "all_annotations_yolov8m.pt_640"]

    reference_boxes = gpd.read_file(os.path.join("..", "data", "map_data", "test_annotations2_sun.geojson"))
    aois_1 = gpd.read_file(os.path.join("..", "data", "map_data", "test_plots.geojson"))
    aois_2 = gpd.read_file(os.path.join("..", "data", "map_data", "aois.geojson"))
    aois_2["aoi_name"] = "galbyveien"
    aois = gpd.GeoDataFrame(pd.concat([aois_1, aois_2], ignore_index=True))
    aois = aois.loc[np.logical_and(pd.notnull(aois["aoi_name"]), aois["aoi_name"] != "NULL"), :]

    for model in models:
        project = os.path.join(path_to_project(model_dir, model))
        predicted_boxes = gpd.read_file(os.path.join(project, "predictions_IoU_th", "predictions.shp"))

        residuals_n = []
        residuals_dens = []
        for _, aoi in aois.iterrows():
            aoi_geom = aoi["geometry"]
            aoi_area = aoi_geom.area / 10000  # Area in ha.
            predictions_within = predicted_boxes[predicted_boxes.geometry.within(aoi_geom)]
            reference_within = reference_boxes[reference_boxes.geometry.within(aoi_geom)]

            n_reference = len(reference_within)
            dens_reference = n_reference / aoi_area
            n_predicted = len(predictions_within)
            dens_predicted = n_predicted / aoi_area

            # Calculate residuals.
            residual_n = n_reference - n_predicted
            residual_dens = dens_reference -dens_predicted
            residuals_n.append(residual_n)
            residuals_dens.append(residual_dens)
        
        aois_results = aois.copy()
        aois_results["residual_n"] = residuals_n
        aois_results["residual_dens"] = residuals_dens
        # Group by AOIs.
        aois_grouped = aois_results.groupby("aoi_name")[["residual_n", "residual_dens"]]
        rmse_aois = aois_grouped.agg(lambda x: np.sqrt(np.mean(np.power(x, 2))))
        rmse_aois = rmse_aois.rename(columns = {"residual_n": "rmse_n", "residual_dens": "rmse_dens"})
        bias_aois = aois_grouped.mean()
        bias_aois = bias_aois.rename(columns = {"residual_n": "bias_n", "residual_dens": "bias_dens"})
        results_aois = pd.concat([rmse_aois, bias_aois], axis = 1)
        # All AOIs.
        aois_all = aois_results.copy()
        aois_all["aoi_name"] = "all"
        aois_all_grouped = aois_all.groupby("aoi_name")[["residual_n", "residual_dens"]]
        rmse_all = aois_all_grouped.agg(lambda x: np.sqrt(np.mean(np.power(x, 2))))
        rmse_all = rmse_all.rename(columns = {"residual_n": "rmse_n", "residual_dens": "rmse_dens"})
        bias_all = aois_all_grouped.mean()
        bias_all = bias_all.rename(columns = {"residual_n": "bias_n", "residual_dens": "bias_dens"})
        results_all = pd.concat([rmse_all, bias_all], axis = 1)

        collected_results = pd.concat([results_aois, results_all])
        collected_results.to_csv(os.path.join(project, "predictions_IoU_th", "metrics.csv"))


if __name__ == "__main__":
    main()

