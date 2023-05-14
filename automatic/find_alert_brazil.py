import warnings
warnings.filterwarnings(action='ignore', category=UserWarning)

import os
import json
import shutil
import geopandas as gpd


import sys

year = sys.argv[1]
month = sys.argv[2]
day = sys.argv[3]
hour = sys.argv[4]
minute = sys.argv[5]

path = os.path.join(minute)
metadata_file = "metadata.csv"

brazil_lower_left = [-28.93576585672869, -70.90469836359233]
brazil_upper_right = [5.696972115053628, -33.84640810546731]

rows = []
with open("metadata.csv", 'a') as metadata:
    for file_name in os.listdir(path):
        full_path = os.path.join(path, file_name)

        # Track values
        flood = False
        json_file = False
        kml_file = False
        in_brazil = False
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
                gpd.io.file.fiona.drvsupport.supported_drivers['KML'] = 'rw'
                gdf = gpd.read_file(kml_path, driver='KML')
                aoi_centroid = gdf.loc[gdf["Name"] == "aoi_polygon", "geometry"].representative_point().values[0]
                lon = int(aoi_centroid.x)
                lat = int(aoi_centroid.y)

                in_brazil = False
                if lon > brazil_lower_left[1] and lon < brazil_upper_right[1]:
                    if lat > brazil_lower_left[0] and lat < brazil_upper_right[0]:
                        in_brazil = True

                if gdf.shape[0] > 1:
                    risk_profiles = True
                else:
                    risk_profiles = False                
            else:
                kml_file = False

        # Write metadata
        metadata.write(f"{year},{month},{day},{hour},{minute},{file_name},{json_file},{kml_file},{flood},{in_brazil},{risk_profiles}\n")
        
print(f"Done with {year}/{month}/{day}/{hour}/{minute}. Deleting data.")
# Delete alert data
shutil.rmtree(path)
