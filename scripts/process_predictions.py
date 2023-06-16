import os

from osgeo import gdal, osr
from shapely.geometry import Polygon
import numpy as np
import pandas as pd
import geopandas as gpd
import shapely

from yolo_conversions import yolo_to_xy


def collect_bounding_boxes(image_path, label_path, buffer_size, tile_index):
    """Collect bounding boxes in tile

    Args:
        image_path (str): Path to image used for prediction.
        label_path (str): Path to labels for predicted image.
        buffer_size (float): Size of buffer used when tiling images.
        tile_index (gdf): GeoDataFrame containing index of tiles.

    Returns:
        gdf: GeoDataFrame with bounding boxes.
    """
    # Get raster metadata.
    r = gdal.Open(image_path)
    proj = osr.SpatialReference(wkt=r.GetProjection())
    EPSG_code = proj.GetAttrValue("AUTHORITY", 1)
    _, xres, _, _, _, yres = r.GetGeoTransform()
    tile_size_m = round(r.RasterXSize * xres)
    tile_size_px = round(tile_size_m / abs(xres))
    img_width = r.RasterXSize
    img_height = r.RasterYSize

    # Process detections.
    with open(label_path) as l:
        coords = yolo_to_xy(l, img_width, img_height)
    tile = tile_index[tile_index["ID"] == os.path.basename(image_path)]

    tile_bbox = tile.total_bounds  # [xmin, ymin, xmax, ymax]

    # Remove overlap.
    tile_inner = tile
    tile_inner.loc[:, "geometry"] = tile_inner.geometry.buffer(-(buffer_size / 2))
    inner_bbox = tile_inner.total_bounds  # [xmin, ymin, xmax, ymax]

    # Create box for each detection
    bboxes = []
    for i in coords:
        X1 = (i[1] * xres) + tile_bbox[0]
        Y1 = (i[2] * yres) + tile_bbox[1] + tile_size_m
        X2 = (i[3] * xres) + tile_bbox[0]
        Y2 = (i[4] * yres) + tile_bbox[1] + tile_size_m

        # Skip if centroid is outside the inner tile.
        X = (X1 + X2) / 2
        Y = (Y1 + Y2) / 2
        if (
            X < inner_bbox[0]
            or X > inner_bbox[2]
            or Y < inner_bbox[1]
            or Y > inner_bbox[3]
        ):
            continue
        # Create polygon.
        lat_point_list = [Y1, Y1, Y2, Y2, Y1]
        lon_point_list = [X1, X2, X2, X1, X1]
        polygon_geom = Polygon(zip(lon_point_list, lat_point_list))
        crs = {"init": "epsg:" + EPSG_code}
        data = {"class": [i[0]], "prob": [i[5]]}
        bbox = gpd.GeoDataFrame(data, crs=crs, geometry=[polygon_geom])
        bboxes.append(bbox)
    if len(bboxes) == 0:  # Tiles with all boxes outside.
        print("No bounding boxes within tile.")
        return None
    bboxes_tile = gpd.GeoDataFrame(pd.concat(bboxes, ignore_index=True))

    return bboxes_tile


def clean_overlapping(bounding_boxes, th=0.7):
    geometries = bounding_boxes["geometry"]

    # Find intersecting geometries.
    intersecting_boxes = np.array(
        [i.intersects(geometries) for i in geometries]
    )  # Check intersects for each box.
    intersecting_pairs = np.transpose(
        np.where(intersecting_boxes)
    )  # Index of intersecting pairs.
    # Remove self-intersects and duplicates.
    intersecting_pairs = intersecting_pairs[
        intersecting_pairs[:, 0] != intersecting_pairs[:, 1], :
    ]  # Remove self-intersects.
    intersecting_pairs = np.sort(intersecting_pairs, axis=1)  # Ignore order.
    intersecting_pairs = np.unique(
        intersecting_pairs, axis=0
    )  # Keep only unique pairs.

    # Solve conflicts.
    print(f"Found {np.shape(intersecting_pairs)[0]} potential overlapping boxes.")
    remove_boxes = []
    for x, y in intersecting_pairs:
        x_geom = geometries[x]
        y_geom = geometries[y]
        iou = (
            shapely.intersection(x_geom, y_geom).area
            / shapely.unary_union([x_geom, y_geom]).area
        )
        if iou >= th:
            x_prob = bounding_boxes.loc[x, "prob"]
            y_prob = bounding_boxes.loc[y, "prob"]
            if x_prob > y_prob:
                remove_boxes.append(y)
            else:
                remove_boxes.append(x)

    # Remove overlapping
    print(f"{len(remove_boxes)} overlapping boxes removed.")
    cleaned_boxes = bounding_boxes.drop(index=remove_boxes)

    return cleaned_boxes
