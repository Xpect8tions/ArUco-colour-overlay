import yaml
from datetime import datetime


i = 0
time_start = datetime.now()
print(f'time_start = {time_start}')
while True:
    time_now = datetime.now()
    # Specify the path to your YAML file
    yaml_file_path = '/home/adriel/cu_ws/src/opcv/config/ids_params.yaml'
    # Open and read the YAML file
    # Read the image
    time_del = (time_now - time_start).total_seconds()
    print(f'time_del = {time_del}')
    if time_del >= 10: 
        break
    
    rob_scan = i

    print(f'rob_scan = {rob_scan}')

    with open(yaml_file_path, 'r') as f:
        yaml_data = yaml.load(f, Loader=yaml.FullLoader)
        key_to_update = 'rob_stat'
        new_value = 0
        updated_data = [{**item, key_to_update: new_value} if key_to_update in item else item for item in yaml_data]

    with open(yaml_file_path,'w') as f:
        yaml.dump(updated_data,f)

    with open(yaml_file_path, 'r') as f:
        yaml_data = yaml.load(f, Loader=yaml.FullLoader)
        for i in range(len(yaml_data)):
            if yaml_data[i]['num'] == rob_scan:
                yaml_data[i]['rob_stat'] = 1

                yaml_data[i-1]['rob_stat'] = 2
                with open(yaml_file_path,'w') as f:
                    yaml.dump(yaml_data,f)
                break
    i += 1
    
print(f'total = {i} iterations')
freq = i/time_del
print(f'frequency of loops = {freq}')
print('while end')

