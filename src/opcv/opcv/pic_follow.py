import cv2 as cv
import cv2.aruco as aruco
import numpy as np
from datetime import datetime

# Read the image
img = cv.imread('collage16.jpg')
det_img = img.copy()
size = img.shape  
det_params = aruco.DetectorParameters()
dictionary = aruco.getPredefinedDictionary(aruco.DICT_ARUCO_ORIGINAL)
detector = aruco.ArucoDetector(dictionary,det_params)
marker_corners, id_list, rejected_candidates = detector.detectMarkers(img)
det = aruco.drawDetectedMarkers(det_img, marker_corners, id_list)
cv.imshow('det',det)
marker_num = 0
for i in marker_corners:
    for list_o_list in i:
        marker_id = id_list[marker_num,0]
        status = marker_id # 1=b, 2=g, 3=r
        # region edit corners
        x0, y0 = list_o_list[0]
        x1, y1 = list_o_list[1]
        x2, y2 = list_o_list[2]
        x3, y3 = list_o_list[3]

        x_diff_0_1 = x0 - x1
        x_diff_1_2 = x1 - x2
        x_diff_2_3 = x2 - x3
        x_diff_3_0 = x3 - x0

        y_diff_0_1 = y0 - y1
        y_diff_1_2 = y1 - y2
        y_diff_2_3 = y2 - y3
        y_diff_3_0 = y3 - y0

        nx0 = x0 - (x_diff_3_0 - x_diff_0_1)/4
        nx1 = x1 - (x_diff_0_1 - x_diff_1_2)/4
        nx2 = x2 - (x_diff_1_2 - x_diff_2_3)/4
        nx3 = x3 - (x_diff_2_3 - x_diff_3_0)/4

        ny0 = y0 - (y_diff_3_0 - y_diff_0_1)/4
        ny1 = y1 - (y_diff_0_1 - y_diff_1_2)/4
        ny2 = y2 - (y_diff_1_2 - y_diff_2_3)/4
        ny3 = y3 - (y_diff_2_3 - y_diff_3_0)/4

        new_corners = [[nx0, ny0],[nx1, ny1],[nx2, ny2],[nx3, ny3]]
        # endregion edit corners

        np_list = np.array(new_corners,dtype=np.float32)
        mask = np.zeros((size),np.uint8)
        cv.fillPoly(mask, [np_list.astype(int)], color=(255, 255, 255))
        roi = cv.bitwise_and(img, mask)

        if status % 4 == 0:
            roi_b, roi_g, roi_r = cv.split(roi)
            roi_g = cv.subtract(roi_g, 25)
            roi_r = cv.subtract(roi_r, 25)
            roi_b = np.clip(roi_b, 0, 255)
            roi_g = np.clip(roi_g, 0, 255)
            roi_r = np.clip(roi_r, 0, 255)
            roi = cv.merge([roi_b,roi_g,roi_r])

        elif status % 3 ==0:
            roi_b, roi_g, roi_r = cv.split(roi)
            roi_r = cv.subtract(roi_r, 25)
            roi_b = cv.subtract(roi_b, 25)
            roi_b = np.clip(roi_b, 0 ,255)
            roi_g = np.clip(roi_g, 0 ,255)
            roi_r = np.clip(roi_r, 0 ,255)
            roi = cv.merge([roi_b,roi_g,roi_r])

        elif status % 2 == 0:
            roi_b, roi_g, roi_r = cv.split(roi)
            roi_g = cv.subtract(roi_g, 25)
            roi_b = cv.subtract(roi_b, 25)
            roi_b = np.clip(roi_b, 0 ,255)
            roi_g = np.clip(roi_g, 0 ,255)
            roi_r = np.clip(roi_r, 0 ,255)
            roi = cv.merge([roi_b,roi_g,roi_r])

        img = cv.subtract(img,mask)
        img = cv.add(img,roi)

        marker_num += 1 # must be last line in for loop

cv.imshow('img',img)
cv.imwrite('tilt_coloured.jpg',img)
cv.imwrite('tilt_det.jpg',det_img)
# cv.imshow('roi',roi)
cv.imwrite('roi.jpg',roi)
# cv.imshow('mask',mask)
cv.imwrite('mask.jpg',mask)
cv.waitKey(0)
cv.destroyAllWindows()
