import requests
from requests.auth import HTTPBasicAuth

# Artifactory details
url = 'http://<artifactory-url>/artifactory'
source_repo = '<source-repo>'
target_repo = '<target-repo>'
username = '<username>'
password = '<password>'

# Get all files in the source repository
response = requests.get(f'{url}/api/storage/{source_repo}', auth=HTTPBasicAuth(username, password))
files = response.json()['children']

# Move each file to the target repository
for file in files:
    source_path = f'{source_repo}/{file["uri"]}'
    target_path = f'{target_repo}/{file["uri"]}'
    move_response = requests.post(
        f'{url}/api/move/{source_path}?to=/{target_path}',
        auth=HTTPBasicAuth(username, password)
    )
    if move_response.status_code == 200:
        print(f'Successfully moved {file["uri"]}')
    else:
        print(f'Failed to move {file["uri"]}: {move_response.content}')
