import requests
from requests.auth import HTTPBasicAuth
import fnmatch

# Artifactory details
artifactory_url = 'http://<artifactory-url>/artifactory'
repo = 'repo1'
source_path = 'path1'
target_path = 'archive'
username = '<username>'
password = '<password>'
folder_pattern = 'CAAP_2023*'

def get_folders_in_path(repo, path):
    """
    Get all folders in the specified path within the repository.
    """
    url = f'{artifactory_url}/api/storage/{repo}/{path}?list&deep=1'
    print(f'Fetching folders from URL: {url}')  # Debugging output
    response = requests.get(url, auth=HTTPBasicAuth(username, password))
    if response.status_code == 200:
        data = response.json()
        print(f'API Response (get_folders_in_path): {data}')  # Debugging output
        return data.get('folders', [])
    else:
        print(f'Failed to fetch folders: {response.status_code} - {response.content.decode()}')
        return []

def get_files_in_folder(repo, folder_uri):
    """
    Get all files within a specific folder in the repository.
    """
    url = f'{artifactory_url}/api/storage/{repo}/{folder_uri}?list&deep=1'
    print(f'Fetching files from URL: {url}')  # Debugging output
    response = requests.get(url, auth=HTTPBasicAuth(username, password))
    if response.status_code == 200:
        data = response.json()
        print(f'API Response (get_files_in_folder): {data}')  # Debugging output
        return data.get('files', [])
    else:
        print(f'Failed to fetch files: {response.status_code} - {response.content.decode()}')
        return []

def move_files(files, repo, source_path, target_path, dry_run=False):
    """
    Move files from source path to target path within the same repository.
    
    :param files: List of files to process
    :param repo: Repository name
    :param source_path: Source path in the repository
    :param target_path: Target path in the repository
    :param dry_run: If True, only prints the actions without performing them
    """
    for file in files:
        source_file_path = f'{repo}/{file["uri"]}'
        target_file_path = source_file_path.replace(source_path, target_path, 1)
        move_url = f'{artifactory_url}/api/move/{source_file_path}?to={target_file_path}'

        if dry_run:
            print(f'DRY RUN: Move {source_file_path} to {target_file_path}')
        else:
            print(f'Attempting to move {source_file_path} to {target_file_path}')
            move_response = requests.post(move_url, auth=HTTPBasicAuth(username, password))
            if move_response.status_code == 200:
                print(f'Successfully moved {file["uri"]}')
            else:
                print(f'Failed to move {file["uri"]}: {move_response.status_code} - {move_response.content.decode()}')

def main(dry_run=False):
    """
    Main function to get folders, list files within those folders, and move them.
    """
    try:
        folders = get_folders_in_path(repo, source_path)
        print(f'Found {len(folders)} folders in {repo}/{source_path}')

        for folder in folders:
            folder_name = folder['uri'].split('/')[-1]
            if fnmatch.fnmatch(folder_name, folder_pattern):
                print(f'Processing folder: {folder["uri"]}')
                files = get_files_in_folder(repo, folder['uri'])
                print(f'Found {len(files)} files in folder {folder["uri"]}')
                move_files(files, repo, source_path, target_path, dry_run)
                
    except requests.exceptions.RequestException as e:
        print(f'Error: {e}')

# Example usage
if __name__ == '__main__':
    dry_run = False  # Set to True for a dry run
    main(dry_run)
