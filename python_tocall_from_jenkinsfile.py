import requests
from requests.auth import HTTPBasicAuth
import fnmatch
import argparse

def get_folders_in_path(artifactory_url, repo, path, auth):
    """
    Get all folders in the specified path within the repository.
    """
    url = f'{artifactory_url}/api/storage/{repo}/{path}?list&deep=1'
    print(f'Fetching folders from URL: {url}')  # Debugging output
    response = requests.get(url, auth=auth)
    response.raise_for_status()
    data = response.json()
    print(f'Raw API Response (get_folders_in_path): {data}')  # Debugging output

    # Extract folders from the response
    folders = [item for item in data.get('files', []) if item.get('uri').endswith('/')]
    return folders

def move_folder(artifactory_url, repo, source_folder_uri, target_folder_path, auth, dry_run=False):
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
        move_response = requests.post(move_url, auth=auth)
        if move_response.status_code == 200:
            print(f'Successfully moved {source_folder_uri}')
        else:
            print(f'Failed to move {source_folder_uri}: {move_response.status_code} - {move_response.content.decode()}')

def main(artifactory_url, repo, source_path, target_path, username, password, folder_pattern, dry_run=False):
    """
    Main function to get folders, filter them by pattern, and move them.
    """
    try:
        auth = HTTPBasicAuth(username, password)
        folders = get_folders_in_path(artifactory_url, repo, source_path, auth)
        print(f'Found {len(folders)} folders in {repo}/{source_path}')

        for folder in folders:
            folder_name = folder['uri'].split('/')[-2]  # Get the folder name
            if fnmatch.fnmatch(folder_name, folder_pattern):
                print(f'Processing folder: {folder["uri"]}')
                move_folder(artifactory_url, repo, folder['uri'], target_path, auth, dry_run)

    except requests.exceptions.RequestException as e:
        print(f'Error: {e}')

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Move folders in Artifactory based on a pattern')
    parser.add_argument('--artifactory-url', required=True, help='URL of the Artifactory server')
    parser.add_argument('--repo', required=True, help='Repository name')
    parser.add_argument('--source-path', required=True, help='Source path in the repository')
    parser.add_argument('--target-path', required=True, help='Target path in the repository')
    parser.add_argument('--username', required=True, help='Artifactory username')
    parser.add_argument('--password', required=True, help='Artifactory password')
    parser.add_argument('--folder-pattern', required=True, help='Pattern for folders to move')
    parser.add_argument('--dry-run', action='store_true', help='Perform a dry run without making changes')

    args = parser.parse_args()
    main(
        artifactory_url=args.artifactory_url,
        repo=args.repo,
        source_path=args.source_path,
        target_path=args.target_path,
        username=args.username,
        password=args.password,
        folder_pattern=args.folder_pattern,
        dry_run=args.dry_run
    )
