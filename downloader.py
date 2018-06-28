#! /usr/local/bin/env python

import requests
import csv
import ftplib
import os
from decimal import *

current_working_directory = os.path.dirname(os.path.abspath(__file__))

modis_categories = {"Modis24": "https://firms.modaps.eosdis.nasa.gov/data/active_fire/c6/csv/MODIS_C6_USA_contiguous_and_Hawaii_24h.csv", "Moids48":"https://firms.modaps.eosdis.nasa.gov/data/active_fire/c6/csv/MODIS_C6_USA_contiguous_and_Hawaii_48h.csv", "Modis7": "https://firms.modaps.eosdis.nasa.gov/data/active_fire/c6/csv/MODIS_C6_USA_contiguous_and_Hawaii_7d.csv"}

viirs_categories = {"Viirs24": "https://firms.modaps.eosdis.nasa.gov/data/active_fire/viirs/csv/VNP14IMGTDL_NRT_USA_contiguous_and_Hawaii_24h.csv", "Viirs48":  "https://firms.modaps.eosdis.nasa.gov/data/active_fire/viirs/csv/VNP14IMGTDL_NRT_USA_contiguous_and_Hawaii_48h.csv", "Viirs7": "https://firms.modaps.eosdis.nasa.gov/data/active_fire/viirs/csv/VNP14IMGTDL_NRT_USA_contiguous_and_Hawaii_7d.csv"}



def download_points(k, v):
    r = requests.get(v)
    output_name = str(k) + ".csv"
    outfile = open(output_name, "w")
    t = r.text.splitlines()
    for line in t[1:]:
        detection = line.split(',')
        if Decimal(45) <= Decimal(detection[0]) <= Decimal(49.5) and Decimal(-125) <= Decimal(detection[1]) <= Decimal(-116.25):
            outfile.write(str(detection) + '\n')
        

for k in modis_categories.keys():
    download_points(k, modis_categories[k])

