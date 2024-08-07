import requests
import json
import argparse
from datetime import datetime, timedelta

def parse_arguments():
    parser = argparse.ArgumentParser(description='Move artifacts based on last download time.')
    parser.add_argument('--artifactory-url', required=True, help='The base URL of the Artifactory.')
    parser.add_argument('--username', required=True, help='Artifactory username.')
    parser.add_argument('--password', required=True, help='Artifactory password.')
    parser.add_argument('--source-repo', required=True, help='Source repository.')
    parser.add_argument('--source-path', required=True, help='Path in the source repository.')
    parser.add_argument('--archive-repo', required=True, help='Archive repository.')
    parser.add_argument('--archive-path', required=True, help='Path in the archive repository.')
    parser.add_argument('--archive-days', type=int, default=90, help='Number of days to consider for last download.')
    parser.add_argument('--dry-run', action='store_true', help='Perform a dry run without moving artifacts.')
    return parser.parse_args()

def get_artifacts(artifactory_url, repo, path, auth):
    url = f"{artifactory_url}/api/storage/{repo}/{path}?list&deep=1"
    response = requests.get(url, auth=auth)
    if response.status_code == 200:
        return response.json().get('files', [])
    else:
        print(f"Failed to list artifacts: {response.text}")
        return []

def get_artifact_metadata(artifactory_url, repo, path, name, auth):
    url = f"{artifactory_url}/api/storage/{repo}/{path}/{name}"
    response = requests.get(url, auth=auth)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to get metadata for {name}: {response.text}")
        return {}

def move_artifact(artifactory_url, source_repo, source_path, name, target_repo, target_path, dry_run, auth):
    source_full_path = f"{source_repo}/{source_path}/{name}"
    target_full_path = f"{target_repo}/{target_path}/{name}"
    url = f"{artifactory_url}/api/move/{source_full_path}?to=/{target_full_path}"
    
    if dry_run:
        print(f"Dry run: {source_full_path} would be moved to {target_full_path}")
        return

    response = requests.post(url, auth=auth)
    if response.status_code == 200:
        print(f"Successfully moved {source_full_path} to {target_full_path}")
    else:
        print(f"Failed to move {source_full_path}: {response.text}")

def main():
    args = parse_arguments()
    auth = (args.username, args.password)

    past_date = datetime.now() - timedelta(days=args.archive_days)
    date_str = past_date.strftime("%Y-%m-%dT%H:%M:%S.000Z")

    artifacts = get_artifacts(args.artifactory_url, args.source_repo, args.source_path, auth)

    for artifact in artifacts:
        if artifact.get('folder', False):
            continue  # Skip folders

        name = artifact.get('uri').split('/')[-1]
        metadata = get_artifact_metadata(args.artifactory_url, args.source_repo, args.source_path, name, auth)
        last_downloaded = metadata.get('lastDownloaded', '')

        if last_downloaded:
            last_downloaded_date = datetime.strptime(last_downloaded, "%Y-%m-%dT%H:%M:%S.%fZ")
            if last_downloaded_date < past_date:
                move_artifact(args.artifactory_url, args.source_repo, args.source_path, name, args.archive_repo, args.archive_path, args.dry_run, auth)
        else:
            print(f"No last download date for {name}")

if __name__ == '__main__':
    main()
