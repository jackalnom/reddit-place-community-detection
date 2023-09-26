import os
import csv
import glob
import shutil

# Path to the input directory and CSV file
input_dir = 'D:/CPM_no_adjacency_000006/'
csv_file = 'D:/mappings.csv'
output_dir = 'D:/remapped_communities/'

# Read the CSV file to create a mapping from numbers to community names
mapping = {}
with open(csv_file, 'r') as f:
    reader = csv.reader(f)
    for row in reader:
        community_name = row[0]
        for number in row[1:]:
            if number != '':
                mapping[int(number)] = community_name

# Iterate over all files in the input directory
for filepath in glob.glob(os.path.join(input_dir, 'cluster users *.txt')):
    # Extract the number from the filename
    number = int(os.path.basename(filepath).split(' ')[2].split('.')[0])

    # Use the mapping to get the corresponding community name
    community_name = mapping.get(number)

    if community_name is not None:
        # Create a new file for the community if it doesn't exist yet
        community_file = os.path.join(output_dir, f'{community_name}.txt')
        if not os.path.exists(community_file):
            open(community_file, 'w').close()

        # Append the contents of the current file to the community file
        with open(community_file, 'a') as cf, open(filepath, 'r') as f:
            shutil.copyfileobj(f, cf)
