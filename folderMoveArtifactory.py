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
    response.raise_for_status()
    data = response.json()
    print(f'Raw API Response (get_folders_in_path): {data}')  # Debugging output

    # Extract folders from the response
    folders = [item for item in data.get('files', [])]
    return folders

def move_folder(repo, source_folder_uri, target_folder_path, dry_run=False):
    """
    Move a folder from source path to target path within the same repository.
    
    :param repo: Repository name
    :param source_folder_uri: URI of the source folder
    :param target_folder_path: Target path in the repository
    :param dry_run: If True, only prints the actions without performing them
    """
    source_folder_path = f'{repo}/{source_folder_uri}'
    target_folder_path_full = source_folder_path.replace(source_path, target_folder_path, 1)
    move_url = f'{artifactory_url}/api/move/{source_folder_path}?to={target_folder_path_full}'

    if dry_run:
        print(f'DRY RUN: Move {source_folder_path} to {target_folder_path_full}')
    else:
        print(f'Attempting to move {source_folder_path} to {target_folder_path_full}')
        move_response = requests.post(move_url, auth=HTTPBasicAuth(username, password))
        if move_response.status_code == 200:
            print(f'Successfully moved {source_folder_uri}')
        else:
            print(f'Failed to move {source_folder_uri}: {move_response.status_code} - {move_response.content.decode()}')

def main(dry_run=False):
    """
    Main function to get folders, filter them by pattern, and move them.
    """
    try:
        folders = get_folders_in_path(repo, source_path)
        print(f'Found {len(folders)} folders in {repo}/{source_path}')

        for folder in folders:
            folder_name = folder['uri'].split('/')[-2]  # Get the folder name
            if fnmatch.fnmatch(folder_name, folder_pattern):
                print(f'Processing folder: {folder["uri"]}')
                move_folder(repo, folder['uri'], target_path, dry_run)

    except requests.exceptions.RequestException as e:
        print(f'Error: {e}')

# Example usage
if __name__ == '__main__':
    dry_run = False  # Set to True for a dry run
    main(dry_run)
