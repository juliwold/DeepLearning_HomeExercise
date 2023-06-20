import geopandas as gpd


def clamp_yolo(coord):
    """Clamp yolo coordinate

    Clamps coordinate outside of 0-1 to 0 or 1.

    Args:
        coord (float): Coordinate to clamp.

    Returns:
        float: Clamped coordinate.
    """
    if coord < 0:
        return 0
    elif coord > 1:
        return 1
    return coord


def utm_to_yolo(gdf, tile_bbox, class_ids):
    """Covert UTM coordinates to YOLO format

    Args:
        gdf (GeoDataFrame): Annotated bounding boxes in tile.
        tile_bbox (list): Bounding box of tile as a list [min_x, min_y, max_x, max_y].
        class_ids (dict): Class ids.

    Returns:
        str: Annotations in YOLO format.
    """
    annotations = []
    # print(gdf["geometry"])
    for _, row in gdf.iterrows():
        if row["geometry"].geom_type == "Polygon":
            polygons = [row["geometry"]]
        else:
            polygons = row["geometry"].geoms
        for pol in polygons:
            vertices = pol.exterior.coords[:]

            # Get extent of tile.
            tile_width_m = round(tile_bbox[2] - tile_bbox[0])
            tile_height_m = round(tile_bbox[3] - tile_bbox[1])

            # Get UTM coordinates of bounding box centre.
            center_x_UTM = sum(coord[0] for coord in vertices) / len(vertices)
            center_y_UTM = sum(coord[1] for coord in vertices) / len(vertices)

            # Convert to coordinates relative to the tile size with origin 0, 0
            # in the upper left corner.
            center_x = center_x_UTM - tile_bbox[0]
            center_y = tile_bbox[3] - center_y_UTM

            # Get width and height of bounding box.
            bbox = pol.bounds  # [min_x, min_y, max_x, max_y]
            width_m = bbox[2] - bbox[0]
            height_m = bbox[3] - bbox[1]

            # Convert coordinates to YOLO
            x = clamp_yolo(center_x / tile_width_m)
            y = clamp_yolo(center_y / tile_height_m)
            w = clamp_yolo(width_m / tile_width_m)
            h = clamp_yolo(height_m / tile_height_m)
            class_id = class_ids[row["class"]]

            yolo_annotation = f"{class_id} {x} {y} {w} {h}\n"
            annotations.append(yolo_annotation)

    return annotations


def yolo_to_xy(labels, img_width, img_height):
    """Convert YOLO coordinates to xy

    Args:
        labels (list): YOLO boxes to convert.
        img_width (int): Image width in pixels.
        img_height (int): Image height in pixels.

    Returns:
        _type_: _description_
    """
    coords = []
    all_coords = []
    for i in labels:
        l = i.split(" ")
        label = int(l[0])
        coords = list(map(float, l[1:6]))
        x1 = float(img_width) * (2.0 * float(coords[0]) - float(coords[2])) / 2.0
        y1 = float(img_height) * (2.0 * float(coords[1]) - float(coords[3])) / 2.0
        x2 = float(img_width) * (2.0 * float(coords[0]) + float(coords[2])) / 2.0
        y2 = float(img_height) * (2.0 * float(coords[1]) + float(coords[3])) / 2.0
        tmp = [label, int(x1), int(y1), int(x2), int(y2), float(coords[4])]
        all_coords.append(list(tmp))
    return all_coords
