# Read the existing Dockerfile
with open('Dockerfile', 'r') as file:
    dockerfile_content = file.read()

# Define the new base image
new_base_image = "ubuntu:20.04"

# Define a regular expression pattern to match all "FROM" instructions
pattern = r'(?i)^FROM\s+\S+'

# Replace all "FROM" instructions with the new base image
dockerfile_content = re.sub(pattern, f'FROM {new_base_image}', dockerfile_content)

# Write the updated Dockerfile
with open('Dockerfile', 'w') as file:
    file.write(dockerfile_content)
