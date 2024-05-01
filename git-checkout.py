#### local branch
import subprocess

def checkout_or_create_branch(branch_name):
    try:
        subprocess.check_output(['git', 'show-ref', '--verify', '--quiet', f'refs/heads/{branch_name}'])
        exists = True
    except subprocess.CalledProcessError:
        exists = False

    if exists:
        print(f"The branch '{branch_name}' exists.")
        subprocess.run(['git', 'checkout', branch_name])
    else:
        print(f"The branch '{branch_name}' does not exist. Creating...")
        subprocess.run(['git', 'checkout', '-b', branch_name])

# Example usage:
branch_name = 'your_branch_name'

checkout_or_create_branch(branch_name)


#### remote branch

import subprocess

def remote_branch_exists(branch_name):
    try:
        # Fetch the remote references
        subprocess.run(['git', 'fetch', '--quiet'], check=True)
        
        # Check if the remote branch exists
        subprocess.check_output(['git', 'rev-parse', f'remotes/origin/{branch_name}'])
        return True
    except subprocess.CalledProcessError:
        return False

# Example usage:
branch_name = 'your_branch_name'

if remote_branch_exists(branch_name):
    print(f"The remote branch '{branch_name}' exists.")
    # Now you can safely checkout the branch
    # subprocess.run(['git', 'checkout', branch_name])
else:
    print(f"The remote branch '{branch_name}' does not exist.")

