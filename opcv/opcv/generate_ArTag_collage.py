import cv2 as cv
import random
import numpy as np

##############################
max_marker_id = 1024
aruco_dict = cv.aruco.getPredefinedDictionary(cv.aruco.DICT_ARUCO_ORIGINAL)
marker_size = 60
image_file_name = 'marker_original_'
image_file_extension = '.png'
collage_name = 'collage.jpg'
collage_dim = [16,16]
##############################


for i in range(max_marker_id):
    image_file_full_name = f"{image_file_name}{i}{image_file_extension}"

    marker_img = cv.aruco.generateImageMarker(aruco_dict, i, marker_size)
    # # cv.imwrite(image_file_full_name,marker_img)
    # cv.imshow('marker_img',marker_img)
    # marker_img = cv.imread(image_file_full_name)

    # print("Dimensions:", marker_img.shape)
order_o_markers = []
max_mark_in_col = collage_dim[0] * collage_dim[1]
for num in range(max_mark_in_col):
    mar_id = random.randint(0,max_marker_id)
    while mar_id in order_o_markers:
        mar_id = random.randint(0,max_marker_id)
    order_o_markers.append(mar_id)
    
print(f'order_o_markers = {order_o_markers}')
print(f'len = {len(order_o_markers)}')
order_o_markers_sort = order_o_markers.copy()
order_o_markers_sort = order_o_markers_sort.sort()
print(f'order_o_markers_sort = {order_o_markers_sort}')

space = int(marker_size/2) #  space between images
collage_size = 16 * marker_size + 16 * space
print(f'collage_size = {collage_size}')
collage = np.ones((collage_size, collage_size, 3), dtype=np.uint8)*255
i = 0
for marker in order_o_markers:
    print(f'i = {i}')
    y = int(np.floor(i/16))
    x = np.remainder(i,16)
    print(f'x,y = {x,y}')
    marker_img = cv.aruco.generateImageMarker(aruco_dict, marker, marker_size)
    marker_img = cv.cvtColor(marker_img, cv.COLOR_GRAY2BGR)
    top = int(space/2 + x*(space + marker_size))
    bottom = int(top + marker_size)
    left = int (space/2 + y*(space + marker_size))
    right = int(left + marker_size)
    print(f'top, bottom, left, right = {top, bottom, left, right}')
    collage[left:right, top:bottom, :] = marker_img
    i += 1
cv.imshow('collage16', collage)
cv.waitKey(0)
cv.imwrite('collage16.jpg', collage)

    

# num_o_tags -= 1
# # Load images


# im1 = random.randint(0,num_o_tags)
# im2 = random.randint(0,num_o_tags)
# im3 = random.randint(0,num_o_tags)
# im4 = random.randint(0,num_o_tags)
# im5 = random.randint(0,num_o_tags)
# im6 = random.randint(0,num_o_tags)
# im7 = random.randint(0,num_o_tags)
# im8 = random.randint(0,num_o_tags)
# im9 = random.randint(0,num_o_tags)
# print (f'im1 = {im1}')
# print (f'im2 = {im2}')
# print (f'im3 = {im3}')
# print (f'im4 = {im4}')
# print (f'im5 = {im5}')
# print (f'im6 = {im6}')
# print (f'im7 = {im7}')
# print (f'im8 = {im8}')
# print (f'im9 = {im9}')
# image1 = cv.imread(f'marker_original_{im1}.png')
# image2 = cv.imread(f'marker_original_{im2}.png')
# image3 = cv.imread(f'marker_original_{im3}.png')
# image4 = cv.imread(f'marker_original_{im4}.png')
# image5 = cv.imread(f'marker_original_{im5}.png')
# image6 = cv.imread(f'marker_original_{im6}.png')
# image7 = cv.imread(f'marker_original_{im7}.png')
# image8 = cv.imread(f'marker_original_{im8}.png')
# image9 = cv.imread(f'marker_original_{im9}.png')

# # Define spaces between images
# space = int(marker_size/2) #  space between images
# print(f'space_x, space_y = {space, space}')

# # Calculate canvas size
# collage_size = 3 * marker_size + 3 * space
# print(f'collage_size = {collage_size}')
# # Create a canvas
# collage = np.ones((collage_size, collage_size, 3), dtype=np.uint8)*255

# # Y-axis values
# top_start = int(space/2)
# top_stop = int(top_start + marker_size)
# y_middle_start = top_stop + space
# y_middle_stop = y_middle_start + marker_size
# bot_start = y_middle_stop + space
# bot_stop = bot_start + marker_size


# # X-axis values
# left_start = int(space/2)
# left_stop = int(left_start + marker_size)
# x_middle_start = int(top_stop + space)
# x_middle_stop = int(x_middle_start + marker_size)
# right_start = int(x_middle_stop + space)
# right_stop = int(right_start+ marker_size)

# # Paste images onto the canvas with spaces
# collage[top_start:top_stop , left_start:left_stop] = image1
# collage[top_start:top_stop, x_middle_start:x_middle_stop] = image2
# collage[top_start:top_stop, right_start:right_stop] = image3

# collage[y_middle_start:y_middle_stop , left_start:left_stop] = image4
# collage[y_middle_start:y_middle_stop, x_middle_start:x_middle_stop] = image5
# collage[y_middle_start:y_middle_stop, right_start:right_stop] = image6

# collage[bot_start:bot_stop , left_start:left_stop] = image7
# collage[bot_start:bot_stop, x_middle_start:x_middle_stop] = image8
# collage[bot_start:bot_stop, right_start:right_stop] = image9
# # Display the collage
# cv.imwrite(collage_name,collage)
# cv.imshow('Collage', collage)
# cv.waitKey(0)
# cv.destroyAllWindows()
