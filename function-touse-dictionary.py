# Function to perform search and replace using the dictionary
def search_replace(file_path, search_replace_dict):
    with open(file_path, 'r') as file:
        file_content = file.read()
    
    # Perform search and replace
    for search_str, replace_str in search_replace_dict.items():
        file_content = file_content.replace(search_str, replace_str)

    with open(file_path, 'w') as file:
        file.write(file_content)
