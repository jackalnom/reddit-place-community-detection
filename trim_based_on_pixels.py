from csv import reader
import csv
import logging
from pathlib import Path
import os
import json
from PIL import Image
import numpy as np
import ast

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s %(levelname)-8s %(message)s",
                    datefmt="%Y-%m-%d %H:%M:%S")

directory = "D:/place 2023"
# Get a list of all CSV files in the directory
csv_files = [f for f in os.listdir(directory) if f.endswith('.csv')]

output_file = open("D:/canada.txt", 'a', newline='')
csvwriter = csv.writer(output_file)
# Loop through each file
for csv_file in csv_files:
    logging.info(f"reading {csv_file}")
    with open(os.path.join(directory, csv_file), 'r') as read_obj:
        csv_reader = reader(read_obj)
        next(csv_reader)
        for line in csv_reader:
            if line[2].startswith('{'):
                continue

            coord = line[2].split(',')

            row = int(coord[0])
            col = int(coord[1])
            if (row > 91 and row < 151 and col > 151 and col < 183):
                csvwriter.writerow(line)

    logging.info("done")
