import requests
import json
from datetime import datetime, timedelta

# Configuration
artifactory_url = "https://<artifactory-url>/artifactory"
username = "<username>"
password = "<password>"
source_repo = "source-repo"
archive_repo = "archive-repo"
archive_path = "/path/to/archive"

# Calculate the date 3 months ago
three_months_ago = datetime.now() - timedelta(days=90)
date_str = three_months_ago.strftime("%Y-%m-%dT%H:%M:%S.000Z")

# AQL query to find artifacts downloaded in the last 3 months
aql_query = f'items.find({{"repo": "{source_repo}", "stat.downloaded": {{"$gt": "{date_str}"}}}})'

# Execute the AQL query
response = requests.post(
    f"{artifactory_url}/api/search/aql",
    auth=(username, password),
    headers={"Content-Type": "text/plain"},
    data=aql_query
)

if response.status_code == 200:
    artifacts = response.json()['results']
    
    for artifact in artifacts:
        repo = artifact['repo']
        path = artifact['path']
        name = artifact['name']
        full_path = f"{repo}/{path}/{name}"

        # Move the artifact
        move_payload = {
            "targetRepo": archive_repo,
            "targetPath": archive_path,
            "dryRun": False
        }

        move_response = requests.post(
            f"{artifactory_url}/api/move/{full_path}",
            auth=(username, password),
            headers={"Content-Type": "application/json"},
            data=json.dumps(move_payload)
        )

        if move_response.status_code == 200:
            print(f"Successfully moved {full_path} to {archive_repo}/{archive_path}")
        else:
            print(f"Failed to move {full_path}: {move_response.text}")
else:
    print(f"Failed to execute AQL query: {response.text}")
