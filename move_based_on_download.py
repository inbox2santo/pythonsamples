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
    parser.add_argument('--archive-repo', required=True, help='Archive repository.')
    parser.add_argument('--archive-path', required=True, help='Path in the archive repository.')
    parser.add_argument('--months', type=int, default=3, help='Number of months to consider for last download.')
    return parser.parse_args()

def main():
    args = parse_arguments()

    # Calculate the date `args.months` months ago
    past_date = datetime.now() - timedelta(days=args.months * 30)
    date_str = past_date.strftime("%Y-%m-%dT%H:%M:%S.000Z")

    # AQL query to find artifacts downloaded in the last `args.months` months
    aql_query = f'items.find({{"repo": "{args.source_repo}", "stat.downloaded": {{"$gt": "{date_str}"}}}})'

    # Execute the AQL query
    response = requests.post(
        f"{args.artifactory_url}/api/search/aql",
        auth=(args.username, args.password),
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
                "targetRepo": args.archive_repo,
                "targetPath": args.archive_path,
                "dryRun": False
            }

            move_response = requests.post(
                f"{args.artifactory_url}/api/move/{full_path}",
                auth=(args.username, args.password),
                headers={"Content-Type": "application/json"},
                data=json.dumps(move_payload)
            )

            if move_response.status_code == 200:
                print(f"Successfully moved {full_path} to {args.archive_repo}/{args.archive_path}")
            else:
                print(f"Failed to move {full_path}: {move_response.text}")
    else:
        print(f"Failed to execute AQL query: {response.text}")

if __name__ == '__main__':
    main()
