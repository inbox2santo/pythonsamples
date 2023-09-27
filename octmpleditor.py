import yaml

def insert_liveness_probe(yaml_data, new_liveness_probe, container_index=0):
    # Ensure the required keys exist
    if (
        "objects" in yaml_data and
        isinstance(yaml_data["objects"], list) and
        len(yaml_data["objects"]) > 0 and
        "spec" in yaml_data["objects"][0] and
        "template" in yaml_data["objects"][0]["spec"] and
        "spec" in yaml_data["objects"][0]["spec"]["template"] and
        "containers" in yaml_data["objects"][0]["spec"]["template"]["spec"] and
        isinstance(yaml_data["objects"][0]["spec"]["template"]["spec"]["containers"], list)
    ):
        containers = yaml_data["objects"][0]["spec"]["template"]["spec"]["containers"]
        if len(containers) > container_index:
            if "livenessProbe" not in containers[container_index]:
                containers[container_index]["livenessProbe"] = new_liveness_probe
                return True
    return False

if __name__ == "__main__":
    input_yaml_file_path = "path/to/your/template.yaml"  # Path to the Template YAML file
    new_liveness_probe = {
        # Define your livenessProbe configuration here
        "httpGet": {
            "path": "/healthz",
            "port": 8080
        },
        "initialDelaySeconds": 30,
        "periodSeconds": 10
    }

    with open(input_yaml_file_path, 'r') as file:
        yaml_data = yaml.safe_load(file)

    if insert_liveness_probe(yaml_data, new_liveness_probe):
        with open(input_yaml_file_path, 'w') as file:
            yaml.dump(yaml_data, file, default_flow_style=False)
        print("LivenessProbe inserted successfully.")
    else:
        print("Failed to insert LivenessProbe. Ensure the YAML structure matches the expected format.")
