from csv import reader
import csv
import logging
from pathlib import Path
import os

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s %(levelname)-8s %(message)s",
                    datefmt="%Y-%m-%d %H:%M:%S")

i = 0
logging.info("building dictionary")

user_file = "D:/canada_communities_CPM/cluster users 0.txt"

with open(user_file, "r") as f:
    user_list = [line.rstrip() for line in f.readlines()]

        # assign users to output file in a dictionary
logging.info("built dictionary")

logging.info("extracting action logs")
directory = "D:/csv"
# Get a list of all CSV files in the directory
csv_files = [f for f in os.listdir(directory) if f.endswith('.csv')]

# Loop through each file
for csv_file in csv_files:
    logging.info(f"reading {csv_file}")
    with open(os.path.join(directory, csv_file),'r',buffering=100000) as f:
        for line in f:
            user_id = line.split(",")[1]
            if user_id in users:
                # Append-adds at last
                in_file.write(line)
            else:
                not_in_file.write(line)
    logging.info("done")
