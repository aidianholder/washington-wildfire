#! /usr/local/bin/env python

from arcgis import ArcGIS
from geojson import dumps, FeatureCollection, Feature
import requests
from bs4 import BeautifulSoup
import xmltodict

NWGCC_layers = ArcGIS("https://services3.arcgis.com/T4QMspbfLg3qTGWY/ArcGIS/rest/services/NWCC_Operational_Layers/FeatureServer")

perimeters = NWGCC_layers.get(2)
outfile = open('current_perimeters.geojson', 'w')
outfile.write(dumps(perimeters))

#def esri_download(service, layer_num, layer_name, file_name)

"""def compose_fire_data():
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
    active_outfile.close()"""


def compose_fire_data():

    x = requests.get('https://gacc.nifc.gov/nwcc/assets/xml/active_fires.xml')
    xml = x.text
    xml_content = xmltodict.parse(xml)
    fires = xml_content['fires']['fire']
    fire_info = {}
    #print('xml fire names')
    for fire in fires:
        fire_name = fire['incident_name'] 
        #print('fire name = ' + fire_name)
        if fire_name.find('(') != -1:
            fire_name = fire_name[:fire_name.find('(')-1]
        fire_hash = {}
        details = ['location', 'percent_contained', 'est_contain_date', 'residences_threatened', 'other_structures_threatened', 'fuel_terrain', 'total_people', 'crews', 'engines', 'helicopters']
        for detail in details:
            fire_hash[detail] = fire[detail]
        fire_info[fire_name] = fire_hash
    large_fires = NWGCC_layers.get(1)
    #outfile = open('large_incidents.geojson', 'w')
    #outfile.write(dumps(large_fires))
    #outfile.close()
    fire_list = large_fires['features']
    active_fires = []
    for fire in fire_list:
        incident_name = fire['properties'].get("FIRE_NM")
        print(incident_name)
        new_details = fire_info.get(incident_name)
        print(new_details)
        if new_details != None:
            for detail in new_details:
                fire['properties'][detail] = new_details.get(detail)
        active_fires.append(fire)
    active_outfile = open('active_incidents.geojson', 'w')
    feature_collection = FeatureCollection(active_fires)
    active_outfile.write(dumps(feature_collection))
    active_outfile.close()
       

compose_fire_data()