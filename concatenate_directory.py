import os

directory = 'D:/boo_canada/'  # Directory containing the files to concatenate
output_file = 'D:/boo_canada.txt'  # Output file

# Get a list of all files in the directory
files = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]

with open(output_file, 'w') as outfile:
    for fname in files:
        with open(os.path.join(directory, fname)) as infile:
            for line in infile:
                outfile.write(line)
