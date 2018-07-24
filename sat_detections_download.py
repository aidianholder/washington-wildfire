#! /usr/local/bin/env python

import requests
import os
from decimal import Decimal
from datetime import datetime, timedelta, tzinfo, timezone
from dateutil import tz
import json
from geojson import Feature, Point, FeatureCollection, dumps

current_working_directory = os.path.dirname(os.path.abspath(__file__))

modis_categories = {"Modis24": "https://firms.modaps.eosdis.nasa.gov/data/active_fire/c6/csv/MODIS_C6_USA_contiguous_and_Hawaii_24h.csv", "Modis48":"https://firms.modaps.eosdis.nasa.gov/data/active_fire/c6/csv/MODIS_C6_USA_contiguous_and_Hawaii_48h.csv", "Modis7": "https://firms.modaps.eosdis.nasa.gov/data/active_fire/c6/csv/MODIS_C6_USA_contiguous_and_Hawaii_7d.csv"}

viirs_categories = {"Viirs24": "https://firms.modaps.eosdis.nasa.gov/data/active_fire/viirs/csv/VNP14IMGTDL_NRT_USA_contiguous_and_Hawaii_24h.csv", "Viirs48":  "https://firms.modaps.eosdis.nasa.gov/data/active_fire/viirs/csv/VNP14IMGTDL_NRT_USA_contiguous_and_Hawaii_48h.csv", "Viirs7": "https://firms.modaps.eosdis.nasa.gov/data/active_fire/viirs/csv/VNP14IMGTDL_NRT_USA_contiguous_and_Hawaii_7d.csv"}


def download_points(k, v):
    r = requests.get(v)
    output_name = str(k) + ".geojson"
    outfile = open(output_name, "w")
    t = r.text.splitlines()
    detections = []
    for line in t[1:]:
        detection = line.split(',')
        #MODIS & VIIRS have same layout for first field: first field - index 0 - of each hit is lat, second is lon, compare vs area of interest in first if statement, proceed or skip if didn't c
        if Decimal(45) <= Decimal(detection[0]) <= Decimal(49.5) and Decimal(-125) <= Decimal(detection[1]) <= Decimal(-116.25):
            if k[0] == "V" and detection[8] != "low" or k[0] == "M" and int(detection[8]) > 30:          
                x = float(detection[0])
                y = float(detection[1])
                modis_point = Point((y, x))
                modis_timestamp = convert_to_pacific_time(detection[5], detection[6])
                modis_confidence = detection[8]
                modis_detection = Feature(geometry=modis_point, properties={"timestamp": modis_timestamp, "confidence": modis_confidence})
                detections.append(modis_detection)
    if len(detections) > 0:
        feature_collection = FeatureCollection(detections)
        outfile.write(dumps(feature_collection))
        
def convert_to_pacific_time(date_field, time_field):
    date_field = date_field.split('-')
    #print(time_field)
    tstamp = [time_field[:2],time_field[2:4]]
    #print(tstamp)
    utc_dt = datetime(int(date_field[0]), int(date_field[1]), int(date_field[2]), int(tstamp[0]), int(tstamp[1]), 0, 0, timezone.utc)
    pacific_time = utc_dt.astimezone(tz.gettz('America/Los_Angeles'))
    pacific_time_string = pacific_time.strftime('%c')
    return pacific_time_string

for k in modis_categories.keys():
    download_points(k, modis_categories[k])

for k in viirs_categories.keys():
    download_points(k, viirs_categories[k])
