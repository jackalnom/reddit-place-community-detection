from csv import reader
import csv
import logging
from pathlib import Path
import os
import json
from PIL import Image
import numpy as np
import ast

def hex_to_rgb(value):
    """Return (red, green, blue) for the color given as #rrggbb."""
    value = value.lstrip('#')
    lv = len(value)
    return tuple(int(value[i:i + lv // 3], 16) for i in range(0, lv, lv // 3))

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s %(levelname)-8s %(message)s",
                    datefmt="%Y-%m-%d %H:%M:%S")

directory = "D:/csv/"
# Get a list of all CSV files in the directory
csv_files = [f for f in os.listdir(directory) if f.endswith('.csv')]

def parse_string(string):
    # Remove the braces and split the string into key-value pairs
    pairs = string.strip('{}').split(', ')

    # Split each pair into a key and a value and store them in a dictionary
    dictionary = {k: int(v) for k, v in (pair.split(': ') for pair in pairs)}

    return dictionary
good_colors = {'#00A368', '#811E9F', '#00CCC0', '#BE0039', '#FFF8B8', '#D4D7D9', '#3690EA', '#6D482F', '#6D001A', '#9C6926', '#00CC78', '#7EED56', '#898D90', '#FFD635', '#6A5CFF', '#FF99AA', '#51E9F4', '#493AC1', '#FFFFFF', '#000000', '#FFB470', '#E4ABFF', '#94B3FF', '#DE107F', '#515252', '#FF4500', '#FF3881', '#2450A4', '#009EAA', '#B44AC0', '#00756F', '#FFA800'}
bad_users = set()
# Loop through each file
for csv_file in csv_files:
    logging.info(f"reading {csv_file}")
    with open(os.path.join(directory, csv_file), 'r') as read_obj:
        csv_reader = reader(read_obj)
        for line in csv_reader:
            if line[3] not in good_colors:
                bad_users.add(line[1])


# write out bad_users
with open("D:/bad_users.txt", 'w') as f:
    for user in bad_users:
        f.write(user + "\n")

