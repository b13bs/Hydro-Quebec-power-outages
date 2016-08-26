#!/usr/bin/python3

import ast
import requests
import sys
import json
import datetime
import pickle
from haversine import haversine
from pprint import pprint

class Location:
    def __init__(self,x,y):
        self.latitude = x
        self.longitude = y


def notify():
    pass


# Compare two lists
def compare_lists(list1, list2):
    if len(list1) is not len(list2):
        return False

    for val in list1:
        if val not in list2:
            return False
    return True


# Make a request to get the list of entries
def parse_webpage():
    current_timestamp = datetime.datetime.now().strftime('%s')
    r = requests.get("http://pannes.hydroquebec.com/pannes/donnees/v2_0/bisversion.json?timeStamp=%s" % current_timestamp)

    if r.status_code is not 200:
        print("[-] HTTP status code: %s" % r.status_code)
        sys.exit()

    time_param = r.text.strip("\"")
    r = requests.get("http://pannes.hydroquebec.com/pannes/donnees/v2_0/bismarkers%s.json" % time_param)
        
    return json.loads(r.text)


# From the list of entries, retrieve entry in function of the coords 
def get_specific_entry(json_obj, coord):
    lat_long, coord_value = coord.split(":")
    index = 1 if lat_long == "lat" else 0
    count = 0
    tmp = []
    for entry in json_obj:
        tmp.append(entry)
        if coord_value in str(ast.literal_eval(entry[4])[index]):
            count += 1
            return_entry = entry

    for elem in tmp:
        print(elem[4])

    if count > 1:
        print("[-] Error with coordinate, more than one results found.")
        sys.exit()
    elif count == 0:
        print("[-] Nothing for that coordinate. Either there are no outages or the coordinates too accurate.")
        sys.exit()
    else:
        return return_entry


#def get_specific_entry(coords_list, coord):
#    for entry in json_obj:


# Given an entry, return the pretty print format
def pretty_entry(entry):
    r = requests.get("http://pannes.hydroquebec.com/pannes/app-mobile/v1_0/causes_status.json")
    status_json = json.loads(r.text)
    try:
        status_msg = status_json['status'][lang][entry[5]]
    except KeyError:
        status_msg = "Inconnu" if lang == "fr" else "Unknown"

    try:
        cause_msg = status_json['cause'][lang][entry[7]]
        if not cause_msg:
            raise KeyError
    except KeyError:
        cause_msg = status_json['cause'][lang]["defaut"]

    return "Nb clients sans élec. : %s\nDébut de la panne : %s\nFin prévue : %s\nCoordonnées [lat,long] : [%s,%s]\n%s\n%s" % (entry[0], entry[1], entry[2], ast.literal_eval(entry[4])[1], ast.literal_eval(entry[4])[0], status_msg, cause_msg)
    
# Main function
if __name__ == "__main__":

    if len(sys.argv) != 2:
        print("[-] Enter one argument following this format: [lat|long]:[0-9]{2}\.[0-9]{2,4}")
        sys.exit()

    coord = sys.argv[1]
    lang = "fr"

    # Load previous entries
    try:
        with open("hydro.pickle", "rb") as handle:
            previous_json_obj = pickle.load(handle)
        current_entry = get_specific_entry(parse_webpage(), coord)
        previous_entry = get_specific_entry(previous_json_obj, coord)

        #print("===PREVIOUS===\n%s\n" % pretty_entry(previous_entry))
        #print("===CURRENT===\n%s\n" % pretty_entry(current_entry))

        if compare_lists(current_entry, previous_entry):
            print("[+] Nothing changed... MOVE ALONG!")
        else:
            print("[-] Change detected! ===Previous===\n%s\n\n===Current===\n%s" % (pretty_entry(previous_entry), pretty_entry(current_entry)))
            #print("[-] Change detected!\n===Previous===\n%s\n\n===Current===\n%s" % (previous_entry, current_entry))
            notify()


    # No pickle exist, create one
    except FileNotFoundError as e:
        print("[+] No previous entry, creating it")
        json_obj = parse_webpage()
        with open("hydro.pickle", "wb") as handle:
            pickle.dump(json_obj, handle)
        print("[+] Entry: %s" % pretty_entry(get_specific_entry(json_obj, coord)))
    
    # Save current dump
    else:
        json_obj = parse_webpage()
        with open("hydro.pickle", "wb") as handle:
            pickle.dump(json_obj, handle)
