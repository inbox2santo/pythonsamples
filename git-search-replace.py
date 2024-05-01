from github import Github
import os
import yaml

def checkout_repository(repo_url, local_path):
    """
    Checkout the repository from GitHub.
    """
    g = Github()  # Assuming you have your GitHub credentials configured
    repo = g.get_repo(repo_url)
    repo_contents = repo.get_contents("")
    os.makedirs(local_path, exist_ok=True)
    for content in repo_contents:
        if content.type == "dir":
            os.makedirs(os.path.join(local_path, content.name), exist_ok=True)
            sub_contents = repo.get_contents(content.path)
            for sub_content in sub_contents:
                if sub_content.type == "file":
                    file_content = sub_content.decoded_content.decode("utf-8")
                    with open(os.path.join(local_path, content.name, sub_content.name), "w") as f:
                        f.write(file_content)

def search_replace_in_files(root_dir, search_string, replace_string):
    """
    Recursively search and replace string in files.
    """
    for root, _, files in os.walk(root_dir):
        for file_name in files:
            file_path = os.path.join(root, file_name)
            with open(file_path, "r") as file:
                content = file.read()
            if search_string in content:
                content = content.replace(search_string, replace_string)
                with open(file_path, "w") as file:
                    file.write(content)

def replace_string_with_yaml(root_dir, yaml_file):
    """
    Replace string in files with value from YAML file.
    """
    with open(yaml_file, "r") as f:
        yaml_data = yaml.safe_load(f)
    for key, value in yaml_data.items():
        search_replace_in_files(root_dir, key, value)

if __name__ == "__main__":
    # Replace these variables with your GitHub repository URL and local directory path
    repository_url = "your/repository-url"
    local_directory = "local-directory"
    
    # Checkout repository
    checkout_repository(repository_url, local_directory)
    
    # Replace string in files with value from YAML file
    yaml_file_path = "path/to/your/yaml/file.yaml"
    replace_string_with_yaml(local_directory, yaml_file_path)
