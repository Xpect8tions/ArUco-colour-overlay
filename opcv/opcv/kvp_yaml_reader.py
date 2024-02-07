import yaml

# Specify the path to your YAML file
yaml_file_path = '/home/adriel/cu_ws/src/opcv/config/ids_params.yaml'

# Open and read the YAML file
with open(yaml_file_path, 'r') as f:
# Load the YAML data
    data = yaml.safe_load(f)


for i in range(len(data)):
    print('---')
    print('num:',data[i]['num'])
    print('id:',data[i]['id'])
