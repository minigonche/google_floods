import warnings
warnings.filterwarnings(action='ignore', category=UserWarning)

import os
import json
import shutil
import geopandas as gpd
from fiona.drvsupport import supported_drivers
supported_drivers['KML'] = 'rw'

import sys

year = sys.argv[1]
month = sys.argv[2]
day = sys.argv[3]
hour = sys.argv[4]
minute = sys.argv[5]

path = os.path.join(minute)
metadata_file = "metadata.csv"

square_lower_left = [13.993500, 87.827824]
square_upper_right = [27.634456, 99.423077]

rows = []
with open("metadata.csv", 'a') as metadata:
    for file_name in os.listdir(path):
        full_path = os.path.join(path, file_name)

        # Track values
        flood = False
        json_file = False
        kml_file = False
        in_square = False
        risk_profiles = False
        

        json_path = os.path.join(full_path, f"{file_name}.json")
        kml_path = os.path.join(full_path, f"{file_name}.kml")

        # Json alert
        if os.path.exists(json_path):
            json_file = True
            f = open(json_path)
            data = json.load(f)
            flooded = data["hasFlooding"]

            if flooded:
                flood = True
        else:
            json_file = False

        # If flood check its in brazil
        if flood:
            if os.path.exists(kml_path):
                kml_file = True
                #gpd.io.file.fiona.drvsupport.supported_drivers['KML'] = 'rw'
                gdf = gpd.read_file(kml_path, driver='KML')
                aoi_centroid = gdf.loc[gdf["Name"] == "aoi_polygon", "geometry"].representative_point().values[0]
                lon = int(aoi_centroid.x)
                lat = int(aoi_centroid.y)

                in_square = False
                if lon > square_lower_left[1] and lon < square_upper_right[1]:
                    if lat > square_lower_left[0] and lat < square_upper_right[0]:
                        in_square = True

                if gdf.shape[0] > 1:
                    risk_profiles = True
                else:
                    risk_profiles = False                
            else:
                kml_file = False

        # Write metadata
        metadata.write(f"{year},{month},{day},{hour},{minute},{file_name},{json_file},{kml_file},{flood},{in_square},{risk_profiles}\n")
        
print(f"Done with {year}/{month}/{day}/{hour}/{minute}. Deleting data.")
# Delete alert data
shutil.rmtree(path)
