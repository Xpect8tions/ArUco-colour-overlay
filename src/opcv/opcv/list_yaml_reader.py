import yaml

# Specify the path to your YAML file
yaml_file_path = '/home/adriel/cu_ws/src/opcv/config/ids_params.yaml'

# Open and read the YAML file
with open(yaml_file_path, 'r') as f:
# Load the YAML data
    data = yaml.safe_load(f)

locations_list = data[0]['locations']
for data in locations_list:
    print(data)