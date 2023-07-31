import pickle

def replace_keys_with_int_inplace(dict_to_convert):
    # Initialize a counter
    counter = 0

    # Create a list of the keys
    keys = list(dict_to_convert.keys())

    # Loop through each key
    for key in keys:
        # Assign the value to a new key in the dictionary
        dict_to_convert[counter] = dict_to_convert.pop(key)

        # Increment the counter
        counter += 1

if __name__ == '__main__':
    # Read the CSV files into a dictionary
    print("reading dict")
    file = open("D:/user_mapping_filtered.pickle",'rb')
    links = pickle.load(file)
    file.close()
    print("read dict")
    print(f"read {len(links)} rows")
    print("filtering dict")
    replace_keys_with_int_inplace(links)
    print(f"filtered to {len(links)} rows")
    print("writing pickle")
    with open('D:/user_mapping_filtered_with_keys.pickle', 'wb') as handle:
        pickle.dump(links, handle, protocol=pickle.HIGHEST_PROTOCOL)
    print("wrote pickle")    