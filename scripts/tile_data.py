import os

from osgeo import gdal, osr
import geopandas as gpd


def tile_orthomosaic(
    input_ortho_path,
    output_path,
    footprints_path,
    tile_size,
    buffer_size,
    path_osgeo_utils,
):
    """Tile orthomosaics.

    Args:
        input_ortho_path (str): Path of orthomosaic to tile.
        output_path (str): Path to directory for writing tiles.
        footprints_path (str): Path to file containing footprint of orthomosaic.
        tile_size (int): Size of tiles in meters.
        buffer_size (int): Size of tile buffer in meters.
        path_osgeo_utils (str): Path to gdal utilities.
    """
    # Read drone acquisition footprints
    footprints = gpd.read_file(footprints_path)
    # Get ortho name
    ortho_name = os.path.splitext(os.path.basename(input_ortho_path))[0]

    # create output dir
    output_tiles_dir = os.path.join(output_path, f"{tile_size}_{ortho_name}")
    if not os.path.exists(output_tiles_dir):
        print(f"Creating output folder '{output_tiles_dir}'...")
        os.makedirs(output_tiles_dir)

    # get raster metadata
    # Get pixel resolution (in meters) and tile size in pixels
    src_ds = gdal.Open(input_ortho_path)  # reads in the orthomosaic
    _, xres, _, _, _, yres = src_ds.GetGeoTransform()  # get pixel size in meters
    print(f"Ortho resolution:{round(xres, 4)} m")
    # Get EPSG code
    proj = osr.SpatialReference(wkt=src_ds.GetProjection())
    EPSG_code = proj.GetAttrValue("AUTHORITY", 1)
    print(f"EPSG code: {EPSG_code}")
    # get number of bands
    n_bands = src_ds.RasterCount
    print(f"Number of bands: {n_bands}")

    # Compute tile and buffer size in pixels
    tile_size_px = round(tile_size / abs(xres))
    buffer_size_px = round(buffer_size / abs(xres))

    # define name for output tile index shapefile
    tileIndex_name = "tile_index"

    # Run gdal_retile.py
    command_retile = (
        "python "
        + path_osgeo_utils
        + "/gdal_retile.py -targetDir "
        + output_tiles_dir
        + " "
        + input_ortho_path
        + " -overlap "
        + str(buffer_size_px)
        + " -ps "
        + str(tile_size_px)
        + " "
        + str(tile_size_px)
        + " -of GTiff -tileIndex "
        + tileIndex_name
        + " -tileIndexField ID"
    )
    print(os.popen(command_retile).read())

    # cleanup tiles
    footprint_ortho = footprints[footprints["filename"] == ortho_name]
    footprint_ortho_UU = footprint_ortho.geometry.unary_union

    # Load tiles shapefile
    tile_index_path = os.path.join(output_tiles_dir, "tile_index.shp")
    tiles = gpd.read_file(tile_index_path)
    tiles = tiles.to_crs(EPSG_code)

    # Select all tiles that are within the boundary polygon
    tiles_in = tiles[tiles.geometry.within(footprint_ortho_UU)]

    # Select all tiles that are not within the boundary polygon
    tiles_out = tiles.loc[~tiles["ID"].isin(tiles_in["ID"])]
    print(f"{len(tiles_out)} tiles to be deleted")

    # delete tiles that are not within the footprint
    gtiffs_delete = [output_tiles_dir + "/" + sub for sub in tiles_out["ID"]]
    for f in gtiffs_delete:
        if os.path.exists(f):
            os.remove(f)
