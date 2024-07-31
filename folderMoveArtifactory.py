import requests
from requests.auth import HTTPBasicAuth
import json

# Artifactory details
artifactory_url = 'http://<artifactory-url>/artifactory'
repo = 'repo1'
source_path = 'path1'
username = '<username>'
password = '<password>'

def get_folders_in_path(repo, path):
    """
    Get all folders in the specified path within the repository.
    """
    url = f'{artifactory_url}/api/storage/{repo}/{path}?list&deep=1'
    print(f'Fetching folders from URL: {url}')  # Debugging output
    response = requests.get(url, auth=HTTPBasicAuth(username, password))
    response.raise_for_status()
    data = response.json()
    print(f'Raw API Response (get_folders_in_path): {json.dumps(data, indent=2)}')  # Debugging output
    return data.get('folders', [])

def main():
    """
    Main function to get folders and print them.
    """
    try:
        folders = get_folders_in_path(repo, source_path)
        print(f'Found {len(folders)} folders in {repo}/{source_path}')
        for folder in folders:
            print(f'Folder: {folder["uri"]}')
    except requests.exceptions.RequestException as e:
        print(f'Error: {e}')

if __name__ == '__main__':
    main()
