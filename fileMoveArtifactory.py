import requests
from requests.auth import HTTPBasicAuth

# Artifactory details
artifactory_url = 'http://<artifactory-url>/artifactory'
repo = 'repo1'
source_path = 'path1'
target_path = 'archive'
username = '<username>'
password = '<password>'
file_pattern = 'CAAP_2023*'

# Function to get all files in the source path
def get_files_in_path(repo, path):
    url = f'{artifactory_url}/api/storage/{repo}/{path}?list&deep=1'
    response = requests.get(url, auth=HTTPBasicAuth(username, password))
    response.raise_for_status()
    return response.json()['files']

# Function to move files from source path to target path within the same repository
def move_files(files, repo, source_path, target_path, pattern):
    for file in files:
        if file['uri'].startswith(f'/{source_path}/{pattern}'):
            source_file_path = f'{repo}/{file["uri"]}'
            target_file_path = source_file_path.replace(source_path, target_path, 1)
            move_url = f'{artifactory_url}/api/move/{source_file_path}?to=/{target_file_path}'
            move_response = requests.post(move_url, auth=HTTPBasicAuth(username, password))
            if move_response.status_code == 200:
                print(f'Successfully moved {file["uri"]}')
            else:
                print(f'Failed to move {file["uri"]}: {move_response.content}')

# Get all files from the source path
try:
    files = get_files_in_path(repo, source_path)
    print(f'Found {len(files)} files in {repo}/{source_path}')
    move_files(files, repo, source_path, target_path, file_pattern)
except requests.exceptions.RequestException as e:
    print(f'Error: {e}')
