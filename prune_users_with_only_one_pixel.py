from collections import Counter
import pickle

def filter_dict(dict_to_filter):
    # Create a Counter object to keep track of the occurrence of each value
    counter = Counter()

    # Count the occurrence of each value
    for value_set in dict_to_filter.values():
        counter.update(value_set)

    # Filter the original dictionary
    return {key: {value for value in value_set if counter[value] > 1}
            for key, value_set in dict_to_filter.items()}

if __name__ == '__main__':
    # Read the CSV files into a dictionary
    print("reading dict")
    file = open("D:/user_mapping_filtered.pickle",'rb')
    links = pickle.load(file)
    file.close()
    print("read dict")
    print(f"read {len(links)} rows")
    print("filtering dict")
    links = filter_dict(links)
    print(f"filtered to {len(links)} rows")
    print("writing pickle")
    with open('D:/user_mapping_filtered_2.pickle', 'wb') as handle:
        pickle.dump(links, handle, protocol=pickle.HIGHEST_PROTOCOL)
    print("wrote pickle")
    # Print the data
    #for key, value in data.items():