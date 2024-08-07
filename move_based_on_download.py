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

def get_artifacts_via_aql(artifactory_url, repo, path, days, auth):
    past_date = (datetime.now() - timedelta(days=days)).isoformat() + 'Z'
    aql_query = f'''
    items.find({
      "repo": "{repo}",
      "path": {{"$match": "{path}/*"}},
      "type": "file",
      "stat.downloaded": {{"$gt": "{past_date}"}}
    }).include("name", "repo", "path", "stat.downloaded")
    '''
    headers = {"Content-Type": "text/plain"}
    response = requests.post(f"{artifactory_url}/api/search/aql", data=aql_query, auth=auth, headers=headers)
    
    if response.status_code == 200:
        return response.json().get('results', [])
    else:
        print(f"Failed to execute AQL query. Status code: {response.status_code}")
        print(f"Response body: {response.text}")
        return []

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
        print(f"Failed to move {source_full_path}. Status code: {response.status_code}")
        print(f"Response body: {response.text}")

def main():
    args = parse_arguments()
    auth = (args.username, args.password)

    artifacts = get_artifacts_via_aql(args.artifactory_url, args.source_repo, args.source_path, args.archive_days, auth)

    for artifact in artifacts:
        name = artifact['name']
        move_artifact(args.artifactory_url, args.source_repo, args.source_path, name, args.archive_repo, args.archive_path, args.dry_run, auth)

if __name__ == '__main__':
    main()
