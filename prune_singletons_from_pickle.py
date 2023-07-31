import pickle
from collections import Counter

def filter_dict(dict_to_filter):
    return {key: value for key, value in dict_to_filter.items() if len(value) > 1}

if __name__ == '__main__':
    # Read the CSV files into a dictionary
    print("reading dict")
    file = open("D:/user_mapping.pickle",'rb')
    links = pickle.load(file)
    file.close()
    print("read dict")
    print(f"read {len(links)} rows")
    print("filtering dict")
    links = filter_dict(links)
    print(f"filtered to {len(links)} rows")
    print("writing pickle")
    with open('D:/user_mapping_filtered.pickle', 'wb') as handle:
        pickle.dump(links, handle, protocol=pickle.HIGHEST_PROTOCOL)
    print("wrote pickle")
    # Print the data
    #for key, value in data.items():