# Read the existing Dockerfile
with open('Dockerfile', 'r') as file:
    dockerfile_content = file.read()

# Define the new commands
new_commands = """
# Your new commands go here
RUN echo 'This is a new command'
RUN apt-get install -y new-package
"""

# Identify the position for insertion (using a marker)
marker = "# INSERT NEW COMMANDS HERE"
insertion_point = dockerfile_content.find(marker)

# Check if the marker exists in the Dockerfile
if insertion_point != -1:
    # Insert a newline and the new commands above the specified position
    dockerfile_content = (
        dockerfile_content[:insertion_point].rstrip() +  # Remove trailing whitespace before the marker
        '\n' + new_commands + '\n' +
        dockerfile_content[insertion_point:]  # Rest of the Dockerfile
    )
else:
    print(f"Marker '{marker}' not found in the Dockerfile.")

# Write the updated Dockerfile
with open('Dockerfile', 'w') as file:
    file.write(dockerfile_content)
