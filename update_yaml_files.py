import yaml

def insert_section_from_yaml(yaml_data, search_key, new_section_yaml_path):
    with open(new_section_yaml_path, 'r') as new_section_file:
        new_section = yaml.safe_load(new_section_file)

    keys = search_key.split(".")
    current_data = yaml_data

    # Traverse the YAML structure to find the parent dictionary where the new section should be added
    for key in keys[:-1]:
        if key in current_data:
            current_data = current_data[key]
        else:
            return False  # The key or path doesn't exist

    # Add the new_section contents to the parent dictionary
    current_data[keys[-1]] = new_section
    return True

if __name__ == "__main__":
    input_yaml_file_path = "path/to/your/input.yaml"  # Path to the input YAML file
    search_key = "spec.metadata.labels"  # Specify the parent key under which you want to insert the new section
    new_section_yaml_path = "path/to/your/new_section.yaml"  # Path to the YAML file containing the new_section content

    with open(input_yaml_file_path, 'r') as file:
        yaml_data = yaml.safe_load(file)

    if insert_section_from_yaml(yaml_data, search_key, new_section_yaml_path):
        with open(input_yaml_file_path, 'w') as file:
            yaml.dump(yaml_data, file, default_flow_style=False)
        print(f"New section inserted under key '{search_key}' from '{new_section_yaml_path}'")
    else:
        print(f"Failed to insert section under key '{search_key}': Key or path doesn't exist")
