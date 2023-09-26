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

directory = "D:/place 2023"
# Get a list of all CSV files in the directory
csv_files = [f for f in os.listdir(directory) if f.endswith('.csv')]
w, h = 3000, 3000
data = np.zeros((h, w, 4), dtype=np.uint8)
count = np.zeros((h, w), dtype=int)
def parse_string(string):
    # Remove the braces and split the string into key-value pairs
    pairs = string.strip('{}').split(', ')

    # Split each pair into a key and a value and store them in a dictionary
    dictionary = {k: int(v) for k, v in (pair.split(': ') for pair in pairs)}

    return dictionary

# Loop through each file
for csv_file in csv_files:
    logging.info(f"reading {csv_file}")
    with open(os.path.join(directory, csv_file), 'r') as read_obj:
        csv_reader = reader(read_obj)
        for line in csv_reader:
            if line[2].startswith('{'):
                json_coord = parse_string(line[2])

                row = int(json_coord["X"])+1500
                col = int(json_coord["Y"])+1500

                count[col, row] += 1
                alpha = 255
                data[col, row] = hex_to_rgb(line[3]) + (alpha,)

    img = Image.fromarray(data, 'RGBA')

    img.save("D:/moderator_actions.png")

    logging.info("done")
