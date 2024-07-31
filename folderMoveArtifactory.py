import subprocess
import json

# Artifactory details
artifactory_url = 'http://<artifactory-url>/artifactory'
repo = 'repo1'
source_path = 'path1'
username = '<username>'
password = '<password>'

def run_curl_command(url):
    """
    Run curl command and return the output.
    """
    result = subprocess.run(
        ['curl', '-u', f'{username}:{password}', '-v', url],
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
    print(f'Raw API Response (get_folders_in_path): {response}')  # Debugging output
    try:
        data = json.loads(response)
        return data.get('folders', [])
    except json.JSONDecodeError as e:
        print(f'Error decoding JSON response: {e}')
        return []

def main():
    """
    Main function to get folders and print them.
    """
    folders = get_folders_in_path_curl(repo, source_path)
    print(f'Found {len(folders)} folders in {repo}/{source_path}')
    for folder in folders:
        print(f'Folder: {folder["uri"]}')

if __name__ == '__main__':
    main()
