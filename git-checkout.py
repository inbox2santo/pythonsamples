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
