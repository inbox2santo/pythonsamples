# Traverse through all files in the repository
for root, dirs, files in os.walk(repo_path):
    for file in files:
        if file.endswith('.py'):  # Modify this condition according to your file types
            file_path = os.path.join(root, file)
            search_replace(file_path, search_replace_dict)
