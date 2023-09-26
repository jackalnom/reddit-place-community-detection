import PIL
import numpy as np
from PIL import Image
from csv import reader
from pathlib import Path
import logging
import os

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s %(levelname)-8s %(message)s",
                    datefmt="%Y-%m-%d %H:%M:%S")

def hex_to_rgb(value):
    """Return (red, green, blue) for the color given as #rrggbb."""
    value = value.lstrip('#')
    lv = len(value)
    return tuple(int(value[i:i + lv // 3], 16) for i in range(0, lv, lv // 3))

dir = "D:/canada_communitieslogs/"
files = Path(dir).glob('cluster pixels *.txt')
for full_file in files:
    w, h = 2000, 2000
    data = np.zeros((h, w, 4), dtype=np.uint8)
    #data[0:256, 0:256] = [255, 0, 0, 255] # red patch in upper left

    # open file in read mode
    with open(str(full_file), 'r') as read_obj:
        # pass the file object to reader() to get the reader object
        csv_reader = reader(read_obj)
        # Iterate over each row in the csv using reader object
        for fields in csv_reader:
            try:
                # row variable is a list that represents a row in csv
                row = int(fields[0])
                col = int(fields[1])
                hex_color = fields[2]

                data[col, row] = hex_to_rgb(hex_color) + (255,)
            except Exception as e:
                logging.error("Caught exception with field (" + str(fields) + ") - " + str(e))

    img = Image.fromarray(data, 'RGBA')
    os.makedirs(dir + "images/", exist_ok=True)
    img.save(dir + "images/" + full_file.name + '.png')
    logging.info("wrote " + full_file.name)