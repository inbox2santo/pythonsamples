import subprocess
import json
from requests.auth import HTTPBasicAuth

# Artifactory details
artifactory_url = 'http://<artifactory-url>/artifactory'
repo = 'repo1'
source_path = 'path1'
username = '<username>'
password = '<password>'
folder_pattern = 'CAAP_2023*'

def run_curl_command(url):
    """
    Run curl command and return the output.
    """
    result = subprocess.run(
        ['curl', '-u', f'{username}:{password}', url],
        capture_output=True, text=True
    )
    if result.returncode != 0:
        print(f'Curl command failed: {result.stderr}')
    return result.stdout

def get_folders_in_path_curl(repo, path):
    """
    Get all folders using curl.
    """
    url = f'{artifactory_url}/api/storage/{repo}/{path}?list&deep=1'
    print(f'Fetching folders with curl from URL: {url}')  # Debugging output
    response = run_curl_command(url)
    data = json.loads(response)
    print(f'API Response (get_folders_in_path): {data}')  # Debugging output
    return data.get('folders', [])

def main():
    """
    Main function to get folders and print them.
    """
    try:
        folders = get_folders_in_path_curl(repo, source_path)
        print(f'Found {len(folders)} folders in {repo}/{source_path}')
        for folder in folders:
            print(f'Folder: {folder["uri"]}')
    except json.JSONDecodeError as e:
        print(f'Error decoding JSON response: {e}')

if __name__ == '__main__':
    main()
