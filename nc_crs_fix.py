"""
Created on Aug 8 2022

@author: Helena Bergstedt, b.geos GmbH
"""

####
# This script imports (ESA CCI Permafrost) netcdf files, copies it, writes the correct CRS string and saves the file as netcdf under a new name.
# ONLY USE if you are sure about the CRS, this is not reprojecting the data, just fixing a broken CRS string
# This script can be used to correct the netcdf files currently available. 

# This is the CRS WKT currently in the published netcdf files: 'PROJCS["WGS 84 / Arctic Polar Stereographic",GEOGCS["WGS 84",DATUM["WGS_1984",SPHEROID["WGS 84",6378137,298.257223563,AUTHORITY["EPSG","7030"]],AUTHORITY["EPSG","6326"]],PRIMEM["Greenwich",0,AUTHORITY["EPSG","8901"]],UNIT["degree",0.0174532925199433,AUTHORITY["EPSG","9122"]],AUTHORITY["EPSG","4326"]],PROJECTION["Polar_Stereographic"],PARAMETER["latitude_of_origin",71],PARAMETER["central_meridian",0],PARAMETER["scale_factor",1],PARAMETER["false_easting",0],PARAMETER["false_northing",0],UNIT["metre",1,AUTHORITY["EPSG","9001"]],AXIS["X",EAST],AXIS["Y",NORTH],AUTHORITY["EPSG","3995"]]'
# The CRS WKT string currently in the files is not valid, can not be read by QGIS/ArcGIS and also creates problems when using gdal within python,
# especially when comparing this data to data from other sources.

# This is the CRS WKT that is needed: 'PROJCS["WGS 84 / Arctic Polar Stereographic", GEOGCS["WGS 84",DATUM["WGS_1984",SPHEROID["WGS 84",6378137,298.257223563]],PRIMEM["Greenwich",0],UNIT["degree",0.0174532925199433,AUTHORITY["EPSG","9122"]],AUTHORITY["EPSG","4326"]],PROJECTION["Polar_Stereographic"],PARAMETER["latitude_of_origin",71],PARAMETER["central_meridian",0],PARAMETER["false_easting",0],PARAMETER["false_northing",0],UNIT["metre",1],AUTHORITY["EPSG","3995"]]'



import rioxarray
from pyproj import CRS
import netCDF4 
import os

# Replace with folder that contains the netcdf files (only the ones you want, otherwise include more filters in the loop)
path = r"C:\Your\Path"

for r,d,f in os.walk(path):
    for fil in f:
        if fil.endswith('.nc') and 'EPSG3995' not in fil:
            print(fil)
            in_path = os.path.join(r, fil)
            # new name for corrected netcdf, change as needed
            out_path = in_path.replace(".nc", "_EPSG3995.nc")

            with netCDF4.Dataset(in_path) as src, netCDF4.Dataset(out_path, "w") as dst:
                # copy global attributes all at once via dictionary
                dst.setncatts(src.__dict__)
                # copy dimensions
                for name, dimension in src.dimensions.items():
                    dst.createDimension(
                        name, (len(dimension) if not dimension.isunlimited() else None))
                # copy all file data 
                for name, variable in src.variables.items():
                    x = dst.createVariable(name, variable.datatype, variable.dimensions)
                    # copy variable attributes all at once via dictionary
                    dst[name].setncatts(src[name].__dict__)
                    dst[name][:] = src[name][:]  
                dst.variables['polar_stereographic'].crs_wkt = 'PROJCS["WGS 84 / Arctic Polar Stereographic", GEOGCS["WGS 84",DATUM["WGS_1984",SPHEROID["WGS 84",6378137,298.257223563]],PRIMEM["Greenwich",0],UNIT["degree",0.0174532925199433,AUTHORITY["EPSG","9122"]],AUTHORITY["EPSG","4326"]],PROJECTION["Polar_Stereographic"],PARAMETER["latitude_of_origin",71],PARAMETER["central_meridian",0],PARAMETER["false_easting",0],PARAMETER["false_northing",0],UNIT["metre",1],AUTHORITY["EPSG","3995"]]'
