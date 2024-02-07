import cv2
import numpy as np
import random

# Load images
image1 = cv2.imread('marker_original_1.png')
image2 = cv2.imread('marker_original_2.png')
image3 = cv2.imread('marker_original_3.png')

# Resize images if needed
width, height = 320, 320
print(f'width, height = {width, height}')
image1 = cv2.resize(image1, (width, height))
image2 = cv2.resize(image2, (width, height))
image3 = cv2.resize(image3, (width, height))

# Define spaces between images
space_x = int(width/2)  # Horizontal space between images
space_y = int(height/2)  # Vertical space between images
print(f'space_x, space_y = {space_x, space_y}')

# Calculate canvas size
collage_width = 3 * width + 3 * space_x
collage_height = height + space_y
print(f'collage_width, collage_height = {collage_width, collage_height}')
# Create a canvas
collage = np.ones((collage_height, collage_width, 3), dtype=np.uint8)*255

# Y-axis values
top_start = int(space_y/2)
top_stop = int(top_start + height)
# y_middle_start = top_stop + space_y
# y_middle_stop = y_middle_start + height
# bot_start = y_middle_stop + space_y
# bot_stop = bot_start + height


# X-axis values
left_start = int(space_x/2)
left_stop = int(left_start + width)
x_middle_start = int(top_stop + space_x)
x_middle_stop = int(x_middle_start + height)
right_start = x_middle_stop + space_x
right_stop = right_start+ width

# Paste images onto the canvas with spaces
collage[top_start:top_stop , left_start:left_stop] = image1
collage[top_start:top_stop, x_middle_start:x_middle_stop] = image2
collage[top_start:top_stop, right_start:right_stop] = image3

# Display the collage
cv2.imshow('Collage', collage)
cv2.waitKey(0)
cv2.destroyAllWindows()
