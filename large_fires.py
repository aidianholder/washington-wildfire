#! /usr/local/bin/env python

from arcgis import ArcGIS
from geojson import dumps, FeatureCollection

NWGCC_layers = ArcGIS("https://services3.arcgis.com/T4QMspbfLg3qTGWY/ArcGIS/rest/services/NWCC_Operational_Layers/FeatureServer")




#outfile = open('large_incidents.geojson', 'w')
#outfile.write(dumps(large_fires))

#perimeters = NWGCC_layers.get(2)

#outfile = open('current_perimeters.geojson', 'w')
#outfile.write(dumps(perimeters))

#def esri_download(service, layer_num, layer_name, file_name)


def compose_fire_details():
    import requests
    from bs4 import BeautifulSoup

    fire_info = {}

    r = requests.get('https://gacc.nifc.gov/nwcc/information/fire_info.aspx')
    t = r.text
    soup = BeautifulSoup(t)
    a = soup.find_all(class_="accordion")
    for incident in a:
        fire_hash = {}
        tables = incident.find_all("table")
        for tb in tables:
            f = tb.find_all("td")
            for c in f:
                k = c.find("label").string
                v = c.find("span").string
                fire_hash[k] = v
        #print(fire_hash)
        fire_info[fire_hash["Incident Name"]] = fire_hash
        #print(fire_info)

    large_fires = NWGCC_layers.get(1)
    fire_list = large_fires['features']
    for fire in fire_list:
        new_details = fire_info.get(fire['properties']['FIRE_NM'])
        print("large fire")
        print(fire)
        print("new details")
        print(new_details)
                
compose_fire_details() 


    


        
