import os
import re
from github import Github

# GitHub credentials
github_username = "your_username"
github_password = "your_password_or_personal_access_token"

# Repository information
repository_owner = "repository_owner"
repository_name = "repository_name"

# Search and replace strings
search_string = "old_string"
replace_string = "new_string"

# Clone the repository locally
repo_path = f"./{repository_name}"
os.system(f"git clone https://github.com/{repository_owner}/{repository_name}.git {repo_path}")

# Function to perform search and replace
def search_replace(file_path, search_str, replace_str):
    with open(file_path, 'r') as file:
        file_content = file.read()
    
    # Perform search and replace
    modified_content = re.sub(search_str, replace_str, file_content)

    with open(file_path, 'w') as file:
        file.write(modified_content)

# Traverse through all files in the repository
for root, dirs, files in os.walk(repo_path):
    for file in files:
        if file.endswith('.py'):  # Modify this condition according to your file types
            file_path = os.path.join(root, file)
            search_replace(file_path, search_string, replace_string)

# Optionally commit and push changes back to GitHub
# Make sure to have the GitHub repository cloned with write permissions
os.chdir(repo_path)
os.system("git add .")
os.system("git commit -m 'Search and replace operation'")
os.system("git push origin master")
