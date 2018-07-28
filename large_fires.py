#! /usr/local/bin/env python

from arcgis import ArcGIS
from geojson import dumps, FeatureCollection, Feature
import requests
from bs4 import BeautifulSoup

NWGCC_layers = ArcGIS("https://services3.arcgis.com/T4QMspbfLg3qTGWY/ArcGIS/rest/services/NWCC_Operational_Layers/FeatureServer")

perimeters = NWGCC_layers.get(2)
outfile = open('current_perimeters.geojson', 'w')
outfile.write(dumps(perimeters))

#def esri_download(service, layer_num, layer_name, file_name)

def compose_fire_data():
    fire_info = {}
    r = requests.get('https://gacc.nifc.gov/nwcc/information/fire_info.aspx')
    t = r.text
    soup = BeautifulSoup(t)
    a = soup.find_all(class_="accordion")
    for incident in a:
        #print(incident)
        fire_hash = {}
        tables = incident.find_all("table")
        for tb in tables:
            f = tb.find_all("td")
            for c in f:
                k = c.find("label").string
                v = c.find("span").string
                fire_hash[k] = v
        fire_info[fire_hash["Incident Name"]] = fire_hash
        #print(fire_hash)
    large_fires = NWGCC_layers.get(1)
    outfile = open('large_incidents.geojson', 'w')
    outfile.write(dumps(large_fires))
    outfile.close()
    fire_list = large_fires['features']
    active_fires = []
    for fire in fire_list:
        incident_name = fire['properties'].get("FIRE_NM")
        new_details = fire_info.get(incident_name)
        if new_details != None:
            details = ['Location', 'Percent Containe', 'Estimated Containment Date', 'Residences Threatened', 'Other Structures Threatened', 'Fuel/Terrain', 'Total People', 'Crews', 'Helicopter', 'Engines']
            for detail in details:
                fire['properties'][detail] = new_details.get(detail)
        active_fires.append(fire)
    active_outfile = open('active_incidents.geojson', 'w')
    feature_collection = FeatureCollection(active_fires)
    active_outfile.write(dumps(feature_collection))
    active_outfile.close()
        

compose_fire_data()