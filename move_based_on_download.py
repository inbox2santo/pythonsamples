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

def main():
    args = parse_arguments()

    # Calculate the date `args.archive_days` days ago
    past_date = datetime.now() - timedelta(days=args.archive_days)
    date_str = past_date.strftime("%Y-%m-%dT%H:%M:%S.000Z")

    # AQL query to find artifacts downloaded in the last `args.archive_days` days
    aql_query = f'items.find({{"repo": "{args.source_repo}", "path": {{"$match" : "{args.source_path}*"}}, "stat.downloaded": {{"$gt": "{date_str}"}}}})'

    print(f"Executing AQL Query: {aql_query}")

    # Execute the AQL query
    response = requests.post(
        f"{args.artifactory_url}/api/search/aql",
        auth=(args.username, args.password),
        headers={"Content-Type": "text/plain"},
        data=aql_query
    )

    print(f"Response Status Code: {response.status_code}")
    print(f"Response Text: {response.text}")

    if response.status_code == 200:
        artifacts = response.json().get('results', [])
        print(f"Found {len(artifacts)} artifacts.")
        
        if not artifacts:
            print("No artifacts found matching the criteria.")
            return
        
        for artifact in artifacts:
            repo = artifact['repo']
            path = artifact['path']
            name = artifact['name']
            full_path = f"{repo}/{path}/{name}"

            # Move the artifact
            move_payload = {
                "targetRepo": args.archive_repo,
                "targetPath": args.archive_path,
                "dryRun": args.dry_run
            }

            move_response = requests.post(
                f"{args.artifactory-url}/api/move/{full_path}",
                auth=(args.username, args.password),
                headers={"Content-Type": "application/json"},
                data=json.dumps(move_payload)
            )

            print(f"Move API Status Code: {move_response.status_code}")
            print(f"Move API Response: {move_response.text}")

            if move_response.status_code == 200:
                if args.dry_run:
                    print(f"Dry run: {full_path} would be moved to {args.archive_repo}/{args.archive_path}")
                else:
                    print(f"Successfully moved {full_path} to {args.archive_repo}/{args.archive_path}")
            else:
                print(f"Failed to move {full_path}: {move_response.text}")
    else:
        print(f"Failed to execute AQL query: {response.text}")

if __name__ == '__main__':
    main()
