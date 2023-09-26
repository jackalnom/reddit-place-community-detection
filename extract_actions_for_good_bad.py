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

users = {}

user_file = "D:/good_vs_bad_pixels_canada.csv"


with open(user_file, "r") as f:
    good_actions_file = open("D:/good/good_actions.txt", 'a')
    bad_actions_file = open("D:/good/bad_actions.txt", 'a')

    csv_reader = csv.reader(f)
    for line in csv_reader:
        user = line[0]
        good_actions = line[1]
        if good_actions == 'good':
            users[user] = good_actions_file
        else:
            users[user] = bad_actions_file
        # assign users to output file in a dictionary
logging.info("built dictionary")

logging.info("extracting action logs")
directory = "D:/place 2023"
#directory = "D:/csv"
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
                users[user_id].write(line)
    logging.info("done")
