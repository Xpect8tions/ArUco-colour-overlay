import cv2 as cv
import cv2.aruco as aruco
import numpy as np
from datetime import datetime

now = datetime.now()
vid_name = f'edge_follow_{now}.mp4'
num = 0
cap = cv.VideoCapture(0)
print('start')
fourcc = cv.VideoWriter_fourcc(*'XVID')
vid_save = cv.VideoWriter(vid_name, fourcc, 30.0, (640, 480))
if not vid_save.isOpened():
    print('could not open video writer')
else:
    print('vid_save.isOpened')
if not cap.isOpened():
    print("Cannot open camera")
    exit()
else:
    print('cap.isOpened')

while True:
    print(f'while start {num}')
    ret, frame = cap.read()
    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
        break
    # Our operations on the frame come here
    # frame = cv.cvtColor(frame,cv.COLOR_BGRA2BGR)
    # Display the resulting frame
    # cv.imshow('raw video', frame)
    if cv.waitKey(1) == 27:
        break
    det_params = aruco.DetectorParameters()
    dictionary = aruco.getPredefinedDictionary(aruco.DICT_ARUCO_ORIGINAL)
    detector = aruco.ArucoDetector(dictionary,det_params)
    marker_corners, id_list, rejected_candidates = detector.detectMarkers(frame)
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

            nx0 = x0 - (x_diff_3_0 - x_diff_0_1)/6
            nx1 = x1 - (x_diff_0_1 - x_diff_1_2)/6
            nx2 = x2 - (x_diff_1_2 - x_diff_2_3)/6
            nx3 = x3 - (x_diff_2_3 - x_diff_3_0)/6

            ny0 = y0 - (y_diff_3_0 - y_diff_0_1)/6
            ny1 = y1 - (y_diff_0_1 - y_diff_1_2)/6
            ny2 = y2 - (y_diff_1_2 - y_diff_2_3)/6
            ny3 = y3 - (y_diff_2_3 - y_diff_3_0)/6

            new_corners = [[nx0, ny0],[nx1, ny1],[nx2, ny2],[nx3, ny3]]
            # endregion edit corners

            np_list = np.array(new_corners,dtype=np.float32)
            mask = np.zeros((480,640,3),np.uint8)
            cv.fillPoly(mask, [np_list.astype(int)], color=(255, 255, 255))
            # cv.imshow('mask',mask)
            roi = cv.bitwise_and(frame, mask)
            cv.imshow('roi', roi)
            # cv.imshow('roi', roi)

            if status == 1:
                print('blue')
                roi_b, roi_g, roi_r = cv.split(roi)
                roi_g = cv.subtract(roi_g, 25)
                roi_r = cv.subtract(roi_r, 25)
                roi_b = np.clip(roi_b, 0, 255)
                roi_g = np.clip(roi_g, 0, 255)
                roi_r = np.clip(roi_r, 0, 255)
                roi = cv.merge([roi_b,roi_g,roi_r])

            elif status == 2:
                print('green')
                roi_b, roi_g, roi_r = cv.split(roi)
                roi_r = cv.subtract(roi_r, 25)
                roi_b = cv.subtract(roi_b, 25)
                roi_b = np.clip(roi_b, 0 ,255)
                roi_g = np.clip(roi_g, 0 ,255)
                roi_r = np.clip(roi_r, 0 ,255)
                roi = cv.merge([roi_b,roi_g,roi_r])

            elif status == 3:
                print('red')
                roi_b, roi_g, roi_r = cv.split(roi)
                roi_g = cv.subtract(roi_g, 25)
                roi_b = cv.subtract(roi_b, 25)
                roi_b = np.clip(roi_b, 0 ,255)
                roi_g = np.clip(roi_g, 0 ,255)
                roi_r = np.clip(roi_r, 0 ,255)
                roi = cv.merge([roi_b,roi_g,roi_r])

            else: print(f'status = {status}')

            frame = cv.subtract(frame,mask)
            frame = cv.add(frame,roi)
            # cv.imshow('new roi', roi)

            marker_num += 1 # must be last line in for loop

    cv.imshow('frame',frame)
    vid_save.write(frame)
    num += 1

cap.release()
vid_save.release()
cv.destroyAllWindows()
