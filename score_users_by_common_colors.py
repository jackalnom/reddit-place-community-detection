import csv
import PIL
import numpy as np
from PIL import Image
from csv import reader
from pathlib import Path
import logging
import os
import concurrent.futures
from collections import defaultdict

# read common colors csv
with open("D:/most_common_colors_canada.csv", 'r') as f:
    reader = csv.reader(f)
    # read most common colors into a dict
    most_common_colors = {}
    for row in reader:
        most_common_colors[row[0] + "," + row[1]] = row[2]
    


logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s %(levelname)-8s %(message)s",
                    datefmt="%Y-%m-%d %H:%M:%S")


dir = "D:/canada_communities_CPM/logs/"

def create_image(full_file):
    #end_date = "2023-07-25 20:30"
    end_date = "2023-07-25 18:30"

    w, h = 61, 33
    #w, h = 3000, 3000
    data = np.zeros((h, w, 4), dtype=np.uint8)
    count = np.zeros((h, w), dtype=int)
    #data[0:256, 0:256] = [255, 0, 0, 255] # red patch in upper left

    good_vs_bad_pixels = defaultdict(lambda: [0, 0])
    # open file in read mode
    with open(str(full_file), 'r') as read_obj:
        # pass the file object to reader() to get the reader object
        csv_reader = csv.reader(read_obj)

        for fields in csv_reader:
            # row variable is a list that represents a row in csv
            if fields[0] < end_date:
                hex_color = fields[3]
                pixel_coord = fields[2]
                user = fields[1]

                if pixel_coord in most_common_colors:
                    if hex_color == most_common_colors[pixel_coord]:
                        good_vs_bad_pixels[user][0] += 1
                    else:
                        good_vs_bad_pixels[user][1] += 1

    # write out good vs bad pixels
    with open("D:/good_vs_bad_pixels_canada.csv", 'w', newline='') as f:
        writer = csv.writer(f)
        for pixel_coord, good_bad in good_vs_bad_pixels.items():
            if good_bad[0] > 2 and good_bad[1] == 0:
                writer.writerow([pixel_coord, 'good'])
            elif good_bad[0] == 0 and good_bad[1] > 1:
                writer.writerow([pixel_coord, 'bad'])

create_image("D:/csv/canada.csv")


