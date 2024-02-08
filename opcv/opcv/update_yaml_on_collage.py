import cv2 as cv
import random
import numpy as np
import yaml
import os

##############################
max_marker_id = 1023
aruco_dict = cv.aruco.getPredefinedDictionary(cv.aruco.DICT_ARUCO_ORIGINAL)
marker_size = 42
collage_dim = [16,16] # x, y
relative_path_to_config = '../config/ids_params.yaml'
relative_path_to_image = 'images/collage16.jpg'
##############################

current_directory = os.path.dirname(os.path.abspath(__file__))
yaml_file_path = os.path.join(current_directory, relative_path_to_config)
path_to_image = os.path.join(current_directory, relative_path_to_image)

print(f'current_directory = {current_directory}')
print(f'path to image = {path_to_image}')
order_o_markers = []
max_num_o_mark_in_coll = collage_dim[0] * collage_dim[1]
print(f'max num o markers in collage = {max_num_o_mark_in_coll}')
for num in range(max_num_o_mark_in_coll):
    mar_id = random.randint(0,max_marker_id)
    while mar_id in order_o_markers:
        mar_id = random.randint(0,max_marker_id)
    order_o_markers.append(mar_id)
    
print(f'order_o_markers = {order_o_markers}')
print(f'len = {len(order_o_markers)}')

space = int(marker_size/2) #  space between images
collage_size_x = collage_dim[0] * marker_size + collage_dim[0] * space
collage_size_y = collage_dim[1] * marker_size + collage_dim[1] * space
print(f'collage_size x, y= {collage_size_x, collage_size_y}')
collage = np.ones((collage_size_y, collage_size_x, 3), dtype=np.uint8)*255
for i in range(len(order_o_markers)):
    print(f'i = {i}')
    y = int(np.floor(i/collage_dim[1]))
    x = i % collage_dim[0]
    print(f'x,y = {x,y}')
    marker_img = cv.aruco.generateImageMarker(aruco_dict, order_o_markers[i], marker_size)
    marker_img = cv.cvtColor(marker_img, cv.COLOR_GRAY2BGR)
    top = int(space/2 + y*(space + marker_size))
    bottom = int(top + marker_size)
    left = int (space/2 + x*(space + marker_size))
    right = int(left + marker_size)
    print(f'top, bottom, left, right = {top, bottom, left, right}')
    collage[top:bottom, left:right,  :] = marker_img
    i += 1
cv.imshow('collage16', collage)
cv.waitKey(0)
cv.imwrite(str(path_to_image), collage)

iteration = 0
list_list = []
write = []
with open(yaml_file_path, 'w') as f:
    yaml.dump(write, f)
for mar_id in order_o_markers:
    data = {}
    
    y = int(np.floor(iteration/collage_dim[1]))
    x = iteration % collage_dim[0]

    print(f'iteration = {iteration}')
    status = [mar_id,[x,y]]
    loc_xy = (iteration % collage_dim[0])+1, int(np.floor(iteration / collage_dim[1])+1)
    print(loc_xy)

    list_list.append(status)

    if iteration == 57 or iteration == 122 or iteration == 136 or iteration == 195:
        shelf_stat = 2
    elif 34<= iteration <=45 or 50 <= iteration<= 61 or 66 <= iteration<= 77 or 114 <= iteration<= 125 or 130 <= iteration<= 141 or 178 <= iteration<= 189 or 194 <= iteration<= 205 or 210 <= iteration<= 221:
        shelf_stat = 1
    elif iteration == 96 or iteration == 112 or iteration == 128 or iteration == 144:
        shelf_stat = -1
    else:
        shelf_stat = 0
    data[mar_id] = [shelf_stat, list(loc_xy)]
    print(f'data = {data}')
    match iteration:
        case 0:
            with open(yaml_file_path, 'w') as f:
                yaml.dump(data, f)
        case _:
            with open(yaml_file_path, 'a') as f:
                yaml.dump(data, f, sort_keys=False)
                
    iteration += 1
    