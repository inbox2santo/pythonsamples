# Read the key-value pair file and create a dictionary
search_replace_dict = {}
with open('search_replace_pairs.txt', 'r') as file:
    for line in file:
        key, value = line.strip().split(',')
        search_replace_dict[key] = value
