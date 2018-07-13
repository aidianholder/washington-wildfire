#! /usr/local/bin/env python

from arcgis import ArcGIS
from geojson import dumps

NWGCC_layers = ArcGIS("https://services3.arcgis.com/T4QMspbfLg3qTGWY/ArcGIS/rest/services/NWCC_Operational_Layers/FeatureServer")

large_fires = NWGCC_layers.get(1)

outfile = open('large_incidents.geojson', 'w')
outfile.write(dumps(large_fires))

perimeters = NWGCC_layers.get(2)

outfile = open('current_perimeters.geojson', 'w')
outfile.write(dumps(perimeters))

#def esri_download(service, layer_num, layer_name, file_name)