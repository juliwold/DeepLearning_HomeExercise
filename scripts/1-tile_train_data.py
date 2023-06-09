import glob

from osgeo import gdal, osr

from tile_data import tile_orthomosaic

def main():
    gdal.UseExceptions()
    path_osgeo_utils = "C:\\NMBU\\Miniconda3\\envs\\deep_learning\\Lib\\site-packages\\GDAL-3.7.0-py3.11-win-amd64.egg-info\\scripts"
    orthomosaics = glob.glob("..\\data\\orthomosaics\\train_data\\*.tif")
    for o in orthomosaics:
        tile_orthomosaic(
            input_ortho_path=o,
            output_path="..\\data\\tiles\\annotations",
            footprints_path="..\\data\\map_data\\drone_acquisitions.geojson",
            tile_size=10,
            buffer_size=0,
            path_osgeo_utils=path_osgeo_utils
        )


if __name__ == "__main__":
    main()
