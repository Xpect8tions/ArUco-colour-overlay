import yaml
import cv2 as cv
import cv2.aruco as aruco
import numpy as np
from datetime import datetime

yaml_file_path = '/home/adriel/cu_ws/src/opcv/config/ids_params.yaml'

time_start = datetime.now()
print(f'time s = {time_start}')
class cngColPic():
    def __init__(self):
        for i in range(10):
            # Read the image
            img = cv.imread('collage16.jpg') # path_to_file = /home/adriel/collage16.jpg
            size = img.shape
            print(f'size = {size}')
            det_params = aruco.DetectorParameters()   
            dictionary = aruco.getPredefinedDictionary(aruco.DICT_ARUCO_ORIGINAL)
            detector = aruco.ArucoDetector(dictionary,det_params)
            det_corners, id_list, rej_cand = detector.detectMarkers(img)
            with open(yaml_file_path, 'r') as f:
                yaml_data = yaml.load(f, Loader=yaml.FullLoader)
            for ind in range(len(yaml_data)):
                mask = None
                print(ind)
                print(mask)
                match yaml_data[ind]['shelf_stat']:
                    case 1:
                        print('case 1 = yaml_data[ind]["shelf_stat"]')
                        marker_id = yaml_data[ind]["id"] # get the id of the marker that has the shelf_stat of 1
                        loc = np.where(np.all(id_list == marker_id, axis=1)) # get location of the id in the scan list
                        print(f'det_corners = {det_corners}')
                        corners = det_corners[loc[0][0]][0]
                        new_corners = self.editCornerSize(corners)
                        # endregion edit corners
                        np_list = np.array(new_corners,dtype=np.float32)
                        mask = np.zeros((size),np.uint8)
                        cv.fillPoly(mask, [np_list.astype(int)], color=(255, 255, 255))
                        roi = cv.bitwise_and(img, mask)
                        roi_b, roi_g, roi_r = cv.split(roi)
                        roi_g = cv.subtract(roi_g, 30)
                        roi_r = cv.subtract(roi_r, 30)
                        roi_b = np.clip(roi_b, 0, 255)
                        roi_g = np.clip(roi_g, 0, 255)
                        roi_r = np.clip(roi_r, 0, 255)
                        roi = cv.merge([roi_b,roi_g,roi_r])

                    case 2:
                        print('case 2 = yaml_data[ind]["shelf_stat"]')
                        marker_id = yaml_data[ind]["id"] # get the id of the marker that has the shelf_stat of 1
                        loc = np.where(np.all(id_list == marker_id, axis=1)) # get location of the id in the scan list
                        corners = det_corners[loc[0][0]][0]
                        np_list = np.array(new_corners,dtype=np.float32)
                        mask = np.zeros((size),np.uint8)
                        cv.fillPoly(mask, [np_list.astype(int)], color=(255, 255, 255))
                        roi = cv.bitwise_and(img, mask)
                        roi_b, roi_g, roi_r = cv.split(roi)
                        roi_r = cv.subtract(roi_r, 30)
                        roi_b = cv.subtract(roi_b, 30)
                        roi_b = np.clip(roi_b, 0 ,255)
                        roi_g = np.clip(roi_g, 0 ,255) 
                        roi = cv.merge([roi_b,roi_g,roi_r])

                    case -1: 
                        print('case -1 = yaml_data[ind]["shelf_stat"]')
                        marker_id = yaml_data[ind]["id"] # get the id of the marker that has the shelf_stat of 1
                        loc = np.where(np.all(id_list == marker_id, axis=1)) # get location of the id in the scan list
                        corners = det_corners[loc[0][0]][0]
                        new_corners = self.editCornerSize(corners)
                        np_list = np.array(new_corners,dtype=np.float32)
                        mask = np.zeros((size),np.uint8)
                        cv.fillPoly(mask, [np_list.astype(int)], color=(255, 255, 255))
                        roi = cv.bitwise_and(img, mask)
                        roi_b, roi_g, roi_r = cv.split(roi)
                        roi_g = cv.subtract(roi_g, 50)
                        roi_b = cv.subtract(roi_b, 50)
                        roi_r = cv.subtract(roi_r, 50)
                        roi_b = np.clip(roi_b, 0 ,255)
                        roi_g = np.clip(roi_g, 0 ,255)
                        roi_r = np.clip(roi_r, 0 ,255)
                        roi = cv.merge([roi_b,roi_g,roi_r])
                
                match yaml_data[ind]['rob_stat']:
                    case 1:
                        marker_id = yaml_data[ind]["id"]
                        loc = np.where(np.all(id_list == marker_id, axis=1)) # get location of the id in the scan list
                        corners = det_corners[loc[0][0]][0]
                        new_corners = self.editCornerSize(corners)
                        np_list = np.array(new_corners,dtype=np.float32)
                        mask = np.zeros((size),np.uint8)
                        cv.fillPoly(mask, [np_list.astype(int)], color=(255, 255, 255))
                        roi = cv.bitwise_and(img, mask)
                        roi_b, roi_g, roi_r = cv.split(roi)
                        roi_g = cv.subtract(roi_g, 20)
                        roi_b = cv.subtract(roi_b, 70)
                        roi_b = np.clip(roi_b, 0 ,255)
                        roi_g = np.clip(roi_g, 0 ,255)
                        roi_r = np.clip(roi_r, 0 ,255)
                        roi = cv.merge([roi_b,roi_g,roi_r])

                    case 2:
                        marker_id = yaml_data[ind]["id"]
                        loc = np.where(np.all(id_list == marker_id, axis=1)) # get location of the id in the scan list
                        corners = det_corners[loc[0][0]][0]
                        new_corners = self.editCornerSize(corners)
                        np_list = np.array(new_corners,dtype=np.float32)
                        mask = np.zeros((size),np.uint8)
                        cv.fillPoly(mask, [np_list.astype(int)], color=(255, 255, 255))
                        roi = cv.bitwise_and(img, mask)
                        roi_b, roi_g, roi_r = cv.split(roi)
                        roi_g = cv.subtract(roi_g, 80)
                        roi_b = cv.subtract(roi_b, 80)
                        roi_b = np.clip(roi_b, 0 ,255)
                        roi_g = np.clip(roi_g, 0 ,255)
                        roi_r = np.clip(roi_r, 0 ,255)
                        roi = cv.merge([roi_b,roi_g,roi_r])

                if mask is not None:
                    img = cv.subtract(img,mask)
                    img = cv.add(img,roi)

                cv.imshow('img',img)
                # cv.waitKey(0) 
                cv.destroyAllWindows()
                cv.imwrite('collage16_colourised.jpg', img)
                print(f'write {i}')
    
        time_end = datetime.now()
        time_elapsed = (time_end - time_start).total_seconds()
        print(f'time spent = {time_elapsed}')
        frequency = 10/time_elapsed
        print(f'frequency = {frequency}Hz')
        
    def editCornerSize(self, corners) -> list:
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

cngColPic()
