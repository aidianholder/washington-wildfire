#! /usr/local/bin/env python

from arcgis import ArcGIS

NCGCC_layers = ArcGIS("https://services3.arcgis.com/T4QMspbfLg3qTGWY/ArcGIS/rest/services/NWCC_Operational_Layers/FeatureServer")

large_fires = NWGCC.get(1)