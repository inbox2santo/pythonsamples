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
file_pattern = 'CAAP_2023*'

def get_files_in_path(repo, path):
    """
    Get all files in the specified path within the repository.
    """
    url = f'{artifactory_url}/api/storage/{repo}/{path}?list&deep=1'
    response = requests.get(url, auth=HTTPBasicAuth(username, password))
    response.raise_for_status()
    return response.json().get('files', [])

def move_files(files, repo, source_path, target_path, pattern, dry_run=False):
    """
    Move files matching the pattern from source path to target path within the same repository.
    
    :param files: List of files to process
    :param repo: Repository name
    :param source_path: Source path in the repository
    :param target_path: Target path in the repository
    :param pattern: Pattern to match files
    :param dry_run: If True, only prints the actions without performing them
    """
    for file in files:
        file_name = file['uri'].split('/')[-1]
        if fnmatch.fnmatch(file_name, pattern):
            source_file_path = f'{repo}/{file["uri"]}'
            target_file_path = source_file_path.replace(source_path, target_path, 1)
            move_url = f'{artifactory_url}/api/move/{source_file_path}?to={target_file_path}'
            
            if dry_run:
                print(f'DRY RUN: Move {source_file_path} to {target_file_path}')
            else:
                move_response = requests.post(move_url, auth=HTTPBasicAuth(username, password))
                if move_response.status_code == 200:
                    print(f'Successfully moved {file["uri"]}')
                else:
                    print(f'Failed to move {file["uri"]}: {move_response.content}')

def main(dry_run=False):
    """
    Main function to get files and move them.
    """
    try:
        files = get_files_in_path(repo, source_path)
        print(f'Found {len(files)} files in {repo}/{source_path}')
        move_files(files, repo, source_path, target_path, file_pattern, dry_run)
    except requests.exceptions.RequestException as e:
        print(f'Error: {e}')

# Example usage
if __name__ == '__main__':
    dry_run = True  # Set to False to perform actual file moves
    main(dry_run)
