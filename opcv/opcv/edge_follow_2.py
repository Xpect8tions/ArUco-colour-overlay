import cv2 as cv
import cv2.aruco as aruco
import numpy as np

class edge_det():
    def __init__(self) -> None:
        # Read the image
        img = cv.imread('slanted.jpg')
        x,y,c = img.shape
        print(f'size = {img.shape}')
        det_params = aruco.DetectorParameters()
        dictionary = aruco.getPredefinedDictionary(aruco.DICT_ARUCO_ORIGINAL)
        detector = aruco.ArucoDetector(dictionary,det_params)
        marker_corners, id_list, rejected_candidates = detector.detectMarkers(img)
        marker_num = 0
        for i in marker_corners:
            for list_o_list in i:
                print('need help')
                marker_id = id_list[marker_num,0]
                status = marker_id # 1=b, 2=g, 3=r
                np_list = np.array(list_o_list,dtype=np.float32)
                mask = np.zeros((x,y,3),np.uint8)
                cv.fillPoly(mask, [np_list.astype(int)], color=(255, 255, 255))
                roi = cv.bitwise_and(img, mask)
                cv.imshow('roi',roi)
                cv.imshow('mask',mask)
                cv.waitKey(0)

                if status == 1:
                    print('blue')
                    for vertical in range(int(y)):
                        for horizontal in range(x):
                            if all(roi[horizontal,vertical]==0) :
                                pass
                            elif roi[horizontal,vertical,0]>=215:
                                roi[horizontal,vertical,1] -= 20
                                roi[horizontal,vertical,2] -= 20
                            else:
                                roi[horizontal,vertical,0] += 40
                        horizontal += 1
                    vertical += 1
                    
                if status == 2:
                    print('green')
                    for vertical in range(int(y)):
                        for horizontal in range(x):
                            if all(roi[horizontal,vertical]==0) :
                                pass
                            elif roi[horizontal,vertical,1]>=215:
                                roi[horizontal,vertical,0] -= 20
                                roi[horizontal,vertical,2] -= 20
                            else:
                                roi[horizontal,vertical,1] += 40

                if status == 3:
                    print('red')
                    for vertical in range(int(y)):
                        for horizontal in range(x):
                            if all(roi[horizontal,vertical]==0) :
                                pass
                            elif roi[horizontal,vertical,2]>=215:
                                roi[horizontal,vertical,0] -= 20
                                roi[horizontal,vertical,1] -= 20
                            else:
                                roi[horizontal,vertical,2] += 40

                                                
                img = cv.subtract(img,mask)
                print('show removed')
                cv.imshow('void',img)
                print('show new roi')
                img = cv.add(img,roi)
        cv.imwrite('slant_coloured.jpg',img)

    # def blue(self,roi):
    #     for y in roi:
    #         for x in y:
    #             if x[0]>=215:
    #                 roi[y,x,1] -= 20
    #                 roi[y,x,2] -= 20
    #             else:
    #                 roi[x,y,0] += 40
    #     return roi

    # def green(self,roi):
    #     for y in roi:
    #         for x in y:
    #             if x[1]>=215:
    #                 roi[y,x,0] -= 20
    #                 roi[y,x,2] -= 20
    #             else:
    #                 roi[y,x,1] += 40

    # def red(self,roi):
    #     for y in roi:
    #         for x in y:
    #             if x[2]>=215:
    #                 roi[y,x,1] -= 20
    #                 roi[y,x,0] -= 20
    #             else: 
    #                 roi[y,x,2] += 40

edge_det() 