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

user_dir = "D:/canada_communities_CPM/"
log_dir = user_dir + "logs/"
os.makedirs(log_dir, exist_ok=True)

files = Path(user_dir).glob('*.txt')
for full_file in files:
    with open(full_file, "r") as f:
        output_file = open(log_dir + full_file.name + ".txt", 'a')

        user_list = [line.rstrip() for line in f.readlines()]

        for user in user_list:
            users[user] = output_file

        # assign users to output file in a dictionary
logging.info("built dictionary")

logging.info("extracting action logs")
#directory = "D:/place 2023"
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
                users[user_id].write(line)
    logging.info("done")
