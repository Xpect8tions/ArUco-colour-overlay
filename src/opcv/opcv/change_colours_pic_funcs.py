import yaml
import cv2 as cv
import cv2.aruco as aruco
import numpy as np
from datetime import datetime

print('start')  
yaml_file_path = '/home/adriel/cu_ws/src/opcv/config/ids_params.yaml'
class chngColPic():
    def __init__(self):
        time_start = datetime.now()
        print('__init__ start')
        # Read the image
        self.img = cv.imread('collage16.jpg') # path_to_file = /home/adriel/collage16.jpg
        size = self.img.shape
        det_params = aruco.DetectorParameters()   
        dictionary = aruco.getPredefinedDictionary(aruco.DICT_ARUCO_ORIGINAL)
        detector = aruco.ArucoDetector(dictionary,det_params)
        marker_corners, id_list, rejected_candidates = detector.detectMarkers(self.img)
        with open(yaml_file_path, 'r') as f:
            yaml_data = yaml.load(f, Loader=yaml.FullLoader)
            print('starting for loop')
        for ind in range(len(yaml_data)):
            roi = None
            match yaml_data[ind]['shelf_stat']:
                case 1:
                    marker_id = yaml_data[ind]["id"] # get the id of the marker that has the shelf_stat of 1
                    loc = np.where(np.all(id_list == marker_id, axis=1)) # get location of the id in the scan list
                    corners = marker_corners[loc[0][0]][0]
                    new_corners = self.editCornerSize(corners)
                    mask, roi = self.editColourBGR(new_corners, size, 0,30,30)

                case 2:
                    marker_id = yaml_data[ind]["id"] # get the id of the marker that has the shelf_stat of 1 
                    loc = np.where(np.all(id_list == marker_id, axis=1)) # get location of the id in the scan list
                    corners = marker_corners[loc[0][0]][0]
                    new_corners = self.editCornerSize(corners)
                    mask, roi = self.editColourBGR(new_corners, size, 30,0,30)

                case -1:
                    marker_id = yaml_data[ind]["id"] # get the id of the marker that has the shelf_stat of 1
                    loc = np.where(np.all(id_list == marker_id, axis=1)) # get location of the id in the scan list
                    corners = marker_corners[loc[0][0]][0]
                    new_corners = self.editCornerSize(corners)
                    mask, roi = self.editColourBGR(new_corners, size, 50,50,50)
            
            match yaml_data[ind]['rob_stat']:
                case 1:
                    marker_id = yaml_data[ind]["id"]
                    loc = np.where(np.all(id_list == marker_id, axis=1)) # get location of the id in the scan list
                    corners = marker_corners[loc[0][0]][0]
                    new_corners = self.editCornerSize(corners)
                    mask, roi = self.editColourBGR(new_corners, size, 0,20,70)

                case 2:
                    marker_id = yaml_data[ind]["id"]
                    loc = np.where(np.all(id_list == marker_id, axis=1)) # get location of the id in the scan list
                    corners = marker_corners[loc[0][0]][0]
                    new_corners = self.editCornerSize(corners)
                    mask, roi = self.editColourBGR(new_corners, size, 100,100,0)

            if roi is not None:
                self.img = cv.subtract(self.img,mask)
                self.img = cv.add(self.img,roi)

        time_end = datetime.now()
        time_elapsed = (time_end - time_start).total_seconds()
        print(f'time spent = {time_elapsed}')
        frequency = 1/time_elapsed
        print(f'frequency = {frequency}Hz')
        cv.imshow('img',self.img)
        cv.waitKey(0)
        cv.destroyAllWindows()
        cv.imwrite('collage16_colourised.jpg', self.img)
        print('write')

    def editColourBGR(self, corners, size, b_sub_val, g_sub_val, r_sub_val):
        np_list = np.array(corners,dtype=np.float32)
        mask = np.zeros((size),np.uint8)
        cv.fillPoly(mask, [np_list.astype(int)], color=(255, 255, 255))
        roi = cv.bitwise_and(self.img, mask)
        roi_b, roi_g, roi_r = cv.split(roi)
        roi_b = cv.subtract(roi_b, b_sub_val)
        roi_g = cv.subtract(roi_g, g_sub_val)
        roi_r = cv.subtract(roi_r, r_sub_val)
        roi_b = np.clip(roi_b, 0, 255)
        roi_g = np.clip(roi_g, 0, 255)
        roi_r = np.clip(roi_r, 0, 255)
        roi = cv.merge([roi_b,roi_g,roi_r])
        return mask, roi
        
    def editCornerSize(self, corners):
        # region edit corners
        x0, y0 = corners[0]
        x1, y1 = corners[1]
        x2, y2 = corners[2]
        x3, y3 = corners[3]

        x_diff_0_1 = x0 - x1
        x_diff_1_2 = x1 - x2
        x_diff_2_3 = x2 - x3
        x_diff_3_0 = x3 - x0

        y_diff_0_1 = y0 - y1
        y_diff_1_2 = y1 - y2
        y_diff_2_3 = y2 - y3
        y_diff_3_0 = y3 - y0

        nx0 = x0 - (x_diff_3_0 - x_diff_0_1)/6
        nx1 = x1 - (x_diff_0_1 - x_diff_1_2)/6
        nx2 = x2 - (x_diff_1_2 - x_diff_2_3)/6
        nx3 = x3 - (x_diff_2_3 - x_diff_3_0)/6

        ny0 = y0 - (y_diff_3_0 - y_diff_0_1)/6
        ny1 = y1 - (y_diff_0_1 - y_diff_1_2)/6
        ny2 = y2 - (y_diff_1_2 - y_diff_2_3)/6
        ny3 = y3 - (y_diff_2_3 - y_diff_3_0)/6

        new_corners = [[nx0, ny0],[nx1, ny1],[nx2, ny2],[nx3, ny3]]
        return new_corners

for i in range(10):
    chngColPic()