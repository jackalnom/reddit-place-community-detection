import os
import csv
from datetime import datetime
import pickle

def read_csvs_to_dict(directory):
    # Create an empty dictionary to hold data
    data = {}

    # Get a list of all CSV files in the directory
    csv_files = [f for f in os.listdir(directory) if f.endswith('.csv')]

    # Loop through each file
    for csv_file in csv_files:
        print(f"reading {csv_file}")
        # Open the CSV file
        with open(os.path.join(directory, csv_file), newline='') as f:
            print(f"opened {csv_file}")
            reader = csv.reader(f)
            print(f"read {csv_file}")
            # Skip the header
            next(reader, None)

            # Loop through each row in the file
            for row in reader:
                # Get the date and hour from the timestamp
                try:
                    timestamp = datetime.strptime(row[0], '%Y-%m-%d %H:%M:%S.%f UTC')
                except ValueError:
                    # If timestamp does not have milliseconds
                    timestamp = datetime.strptime(row[0], '%Y-%m-%d %H:%M:%S UTC')
                
                date_hour = timestamp.strftime('%Y-%m-%d %H')

                # Get the pixel color and coordinates
                pixel_color = row[3]
                coordinates = row[2]

                # Create the key
                key = f"{date_hour},{pixel_color},{coordinates}"

                # If the key isn't in the dictionary, add it with an empty list
                if key not in data:
                    data[key] = set()

                # Add the user to the list for this key
                data[key].add(row[1])

    return data

if __name__ == '__main__':
    # Read the CSV files into a dictionary
    data = read_csvs_to_dict('D:/csv')
    print(f"read {len(data)} rows")
    print("writing pickle")
    with open('D:/canada.pickle', 'wb') as handle:
        pickle.dump(data, handle, protocol=pickle.HIGHEST_PROTOCOL)
    print("wrote pickle")
    # Print the data
    #for key, value in data.items():
    #    print(f'{key}: {value}')