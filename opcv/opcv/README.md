# /opcv

This package consists of the files that create and analyse the ArUco collage images.

## update_yaml_on_collage.py

This file creates a 16 x 16 collage of ArUco markers. once the collage has been created a window will popup, showing you the image of the collage. you can press any button to close the file. once the file has been closed, the yaml file will be updated based on the layout of the image you have seen, and the file will be saved in [/opcv/opcv/images](./images/) as `collage16.jpg`.
Once this file has been created, you can proceed to run the next file to see how the data in the YAML file will affect the colour of the aruco markers.
For more details on the YAML file data, [click here](../config/README.md)

## change_colours\_\*.py

These files are the files that are supposed to analyse the aruco collages. It will scan the `collage16.jpg` photo for ArUco markers. It will then overlay the colours on to the image and show you the new image with the overlay.
The colour value changes by 40 for each channel if only 2 colours need to be changed.
Once you are happy with the results, you can press any button to close the image. it will save as `collage16_colourised.jpg` (only for `change_colours_pic.py`) in [the same folder as collage16.jpg](./images/)
(unable to make change_colours_vid.py work.)
