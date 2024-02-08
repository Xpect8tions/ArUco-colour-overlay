import yaml
import cv2 as cv
import cv2.aruco as aruco
import numpy as np
from datetime import datetime

yaml_file_path = '/path/to/your/folder/ArUco-colour-overlay/opcv/opcv/config/ids_params.yaml'

class cngColPic():
    def __init__(self):
        time_start = datetime.now()
        self.mask = None
        # Read the image
        self.img = cv.imread('collage16.jpg') # path_to_file = /home/adriel/collage16.jpg
        self.size = self.img.shape
        print(f'size = {self.size}')
        det_params = aruco.DetectorParameters()   
        dictionary = aruco.getPredefinedDictionary(aruco.DICT_ARUCO_ORIGINAL)
        detector = aruco.ArucoDetector(dictionary,det_params)
        det_corners, id_list, rej_cand = detector.detectMarkers(self.img)
        with open(yaml_file_path, 'r') as f:
            yaml_data = yaml.load(f, Loader=yaml.FullLoader)

        list_len = len(id_list)
        for i in range(list_len):
            mar_id = id_list[i][0]
            marker_stat = yaml_data[mar_id]
            stat = marker_stat[0]
            corners = det_corners[i][0]
            new_corners = self.editCornerSize(corners)
            match stat:
                case 1: # shelf no bot (blue)
                    self.changeMrkCol(new_corners, 0, 40, 40)
                case 2: # target shelf no bot (green)
                    corners = det_corners[i][0]
                    new_corners = self.editCornerSize(corners)
                    self.changeMrkCol(new_corners, 40, 0, 40)
                case 3: # shelf no bot (orange)
                    self.circleCol(stat, corners, 1,1,1)
                    corners = det_corners[i][0]
                    new_corners = self.editCornerSize(corners)
                    self.changeMrkCol(new_corners, 40, 0, 40)
                case 4: # bot under shelf (ornge in blue)
                    corners = det_corners[i][0]
                    new_corners = self.editCornerSize(corners)
                    self.changeMrkCol(new_corners, 40, 0, 40)
                case 5: # bot under target shelf (ornge in green)
                    corners = det_corners[i][0]
                    new_corners = self.editCornerSize(corners)
                    self.changeMrkCol(new_corners, 40, 0, 40)
                case 6: # bot lifting no shelf (red)
                    corners = det_corners[i][0]
                    new_corners = self.editCornerSize(corners)
                    self.changeMrkCol(new_corners, 40, 0, 40)
                case 7: # bot lifting shelf (red in blue)
                    corners = det_corners[i][0]
                    new_corners = self.editCornerSize(corners)
                    self.changeMrkCol(new_corners, 40, 0, 40)
                case 8: # bot lifting target shelf (red in green)
                    corners = det_corners[i][0]
                    new_corners = self.editCornerSize(corners)
                    self.changeMrkCol(new_corners, 40, 0, 40)
                case -1: # goal no bot (blk)
                    corners = det_corners[i][0]
                    new_corners = self.editCornerSize(corners)
                    self.changeMrkCol(new_corners, 40, 40, 40)
                case -2: # goal with bot (ornge in blk)
                    corners = det_corners[i][0]
                    new_corners = self.editCornerSize(corners)
                    self.changeMrkCol(new_corners, 40, 0, 40)
                case -3: # goal with bot carrying (red in blk)
                    corners = det_corners[i][0]
                    new_corners = self.editCornerSize(corners)
                    self.changeMrkCol(new_corners, 40, 0, 40)
            
            if self.mask is not None:
                self.img = cv.subtract(self.img,self.mask)
                self.img = cv.add(self.img,self.roi)

        time_end = datetime.now()
        time_elapsed = (time_end - time_start).total_seconds()
        print(f'time spent = {time_elapsed}')
        frequency = 10/time_elapsed
        print(f'frequency = {frequency}Hz')

        cv.imshow('img',self.img)
        cv.waitKey(0) 
        cv.destroyAllWindows()
        cv.imwrite('collage16_colourised.jpg', self.img)
        print(f'write')

    def circleCol(self, stat, corners, b, g, r):
        from sympy import symbols, Eq, solve
        
        x, y = symbols('x y')

        top1, left1 = corners[0]
        bot1, right1 = corners[2]
        top2, right2 = corners[1]
        bot2, left2 = corners[3]

        grad1 = (top1 - bot1)/ (left1 - right1)
        grad2 = (top2 - bot2)/ (left2 - right2)

        intcpt1 = top1 - grad1 * left1
        intcpt2 = top2 - grad2 * left2

        graph1 = Eq(grad1 * x + intcpt1, y)
        graph2 = Eq(grad2 * x + intcpt2, y)

        center = solve((graph1, graph2), (x,y))

        corners = np.append(corners,center)
        
        ellipse = cv.fitEllipse(corners)

        print(f'solution = {center}')
        round_mask = cv.ellipse(self.mask,ellipse(255,255,255), -1)
        cv.imshow(round_mask)
        cv.waitKey(0)

    def changeMrkCol(self, new_corners, b, g, r):
        np_list = np.array(new_corners,dtype=np.float32)
        self.mask = np.zeros((self.size),np.uint8)
        cv.fillPoly(self.mask, [np_list.astype(int)], color=(255, 255, 255))
        self.roi = cv.bitwise_and(self.img, self.mask)
        roi_b, roi_g, roi_r = cv.split(self.roi)
        roi_b = cv.subtract(roi_b, b)
        roi_g = cv.subtract(roi_g, g)
        roi_r = cv.subtract(roi_r, r)
        roi_b = np.clip(roi_b, 0 ,255)
        roi_g = np.clip(roi_g, 0 ,255)
        roi_r = np.clip(roi_r, 0 ,255)
        self.roi = cv.merge([roi_b,roi_g,roi_r])

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

        nx0 = x0 - (x_diff_3_0 - x_diff_0_1)/5
        nx1 = x1 - (x_diff_0_1 - x_diff_1_2)/5
        nx2 = x2 - (x_diff_1_2 - x_diff_2_3)/5
        nx3 = x3 - (x_diff_2_3 - x_diff_3_0)/5

        ny0 = y0 - (y_diff_3_0 - y_diff_0_1)/5
        ny1 = y1 - (y_diff_0_1 - y_diff_1_2)/5
        ny2 = y2 - (y_diff_1_2 - y_diff_2_3)/5
        ny3 = y3 - (y_diff_2_3 - y_diff_3_0)/5

        new_corners = [[nx0, ny0],[nx1, ny1],[nx2, ny2],[nx3, ny3]]
        return new_corners

cngColPic()
