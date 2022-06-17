import PIL
import numpy as np
from PIL import Image
from csv import reader
from pathlib import Path
import logging
import os
import concurrent.futures

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s %(levelname)-8s %(message)s",
                    datefmt="%Y-%m-%d %H:%M:%S")


def hex_to_rgb(value):
    """Return (red, green, blue) for the color given as #rrggbb."""
    value = value.lstrip('#')
    lv = len(value)
    return tuple(int(value[i:i + lv // 3], 16) for i in range(0, lv, lv // 3))

dir = "D:/communities_CPM_no_adjacency_0000065/logs/"

def create_image(full_file):
    end_date = "2022-04-04 20:00"

    w, h = 2000, 2000
    data = np.zeros((h, w, 4), dtype=np.uint8)
    count = np.zeros((h, w, 1), dtype=int)
    #data[0:256, 0:256] = [255, 0, 0, 255] # red patch in upper left

    # open file in read mode
    with open(str(full_file), 'r') as read_obj:
        # pass the file object to reader() to get the reader object
        csv_reader = reader(read_obj)
        # Iterate over each row in the csv using reader object
        sortedlist = sorted(csv_reader, key=lambda row: row[0])

        for fields in sortedlist:
            try:
                # row variable is a list that represents a row in csv
                if fields[0] < end_date:
                    hex_color = fields[2]
                    coord = fields[3].split(',')

                    row = int(coord[0])
                    col = int(coord[1])

                    count[col, row] += 1
                    alpha = min(10, count[col, row])*25.5
                    data[col, row] = hex_to_rgb(hex_color) + (alpha,)
            except Exception as e:
                logging.error("Caught exception with field (" + str(fields) + ") - " + str(e))

    img = Image.fromarray(data, 'RGBA')
    os.makedirs(dir + "images/", exist_ok=True)
    img.save(dir + "images/" + full_file.name + '.png')
    logging.info("wrote " + full_file.name)

if __name__ == '__main__':
    logging.info("starting " + dir)
    with concurrent.futures.ProcessPoolExecutor() as executor:
        files = Path(dir).glob('*.txt')
        pool = executor.map(create_image, files)


