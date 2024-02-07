import yaml

# Specify the path to your YAML file
yaml_file_path = '/home/adriel/cu_ws/src/opcv/config/ids_params.yaml'

# Open and read the YAML file
with open(yaml_file_path, 'r') as f:
# Load the YAML data
    data = yaml.load(f,yaml.SafeLoader)

# Access the data as a Python dictionary
for i in range(len(data)):
    if i < 10:
        i = f'00{i}'
    elif i < 100:
        i = f'0{i}'
    else:
        i = str(i)
    print(f'i = {i}')
    print(f"item_{i} = {data[f'location_{i}']}")

data['locations_214'] = 1

with open(yaml_file_path, 'w') as f:
    yaml.dump(data, f)
print(f"data = {data['location_214']}")