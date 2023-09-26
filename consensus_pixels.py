import PIL
import numpy as np
from PIL import Image
from csv import reader
from pathlib import Path
import logging
import os
import concurrent.futures
from collections import defaultdict
import operator

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s %(levelname)-8s %(message)s",
                    datefmt="%Y-%m-%d %H:%M:%S")


def hex_to_rgb(value):
    """Return (red, green, blue) for the color given as #rrggbb."""
    value = value.lstrip('#')
    lv = len(value)
    return tuple(int(value[i:i + lv // 3], 16) for i in range(0, lv, lv // 3))

dir = "D:/canada_communities_CPM/logs/"

def create_image(full_file):
    #end_date = "2023-07-25 20:30"
    end_date = "2023-07-25 18:30"

    w, h = 61, 33
    #w, h = 3000, 3000
    data = np.zeros((h, w, 4), dtype=np.uint8)
    count = np.zeros((h, w), dtype=int)
    pixel_dict = defaultdict(lambda: defaultdict(int))

    #data[0:256, 0:256] = [255, 0, 0, 255] # red patch in upper left

    # open file in read mode
    with open(str(full_file), 'r') as read_obj:
        # pass the file object to reader() to get the reader object
        csv_reader = reader(read_obj)
        # Iterate over each row in the csv using reader object

        for fields in csv_reader:
            try:
                # row variable is a list that represents a row in csv
                if fields[0] < end_date:
                    pixel_dict[fields[2]][fields[3]] += 1
#row = int(coord[0])+1500
                    #col = int(coord[1])+1500
            except Exception as e:
                logging.error("Caught exception with field (" + str(fields) + ") - " + str(e))

    most_common_colors = {}
    for pixel, color_dict in pixel_dict.items():
        total = sum(color_dict.values())
        most_common_color, count = max(color_dict.items(), key=operator.itemgetter(1))
        if (count / total) * 100 > 75 and count > 10:
            most_common_colors[pixel] = {'color': most_common_color, 'percentage': (count / total) * 100, 'count': count}

    print(most_common_colors)
    # write most common colors out as a csv
    with open("D:/most_common_colors_canada.csv", 'w') as f:
        for pixel, color_dict in most_common_colors.items():
            f.write(pixel + "," + color_dict['color'] + "\n")

if __name__ == '__main__':
    logging.info("starting " + dir)
    with concurrent.futures.ProcessPoolExecutor() as executor:
        files = Path(dir).glob('cluster users 0.txt.txt')
        pool = executor.map(create_image, files)


