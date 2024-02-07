import cv2 as cv
import cv2.aruco as aruco
import numpy as np

class edge_det():
    def __init__(self) -> None:
        # Read the image
        self.img = cv.imread('legs.jpeg')
        cv.imshow('legs.jpeg',self.img)
        print(f'size = {self.img.shape}')
        det_params = aruco.DetectorParameters()
        dictionary = aruco.getPredefinedDictionary(aruco.DICT_ARUCO_ORIGINAL)
        detector = aruco.ArucoDetector(dictionary,det_params)
        marker_corners, id_list, rejected_candidates = detector.detectMarkers(self.img)
        marker_num = 0
        for i in marker_corners:
            for list_o_list in i:
                print (f'list_o_list = {list_o_list}')
                mar_id = id_list[marker_num,0] # id_list looks like: [[1] [4] [2] [3]]. mar_id is an int
                print(f'mar_id = {mar_id}')
                status = mar_id
                top_cor = 9999
                bot_cor = -1
                left_cor = 9999
                right_cor = -1
                
                print(f'status = {status}')
                for corner in list_o_list:
                    if corner.size == 0:
                        break
                    else:
                        if top_cor > corner[1]:
                            top_cor = corner[1]
                        elif bot_cor < corner[1]:
                            bot_cor = corner[1]
                        if left_cor > corner[0]:
                            left_cor = corner[0]
                        elif right_cor < corner[0]:
                            right_cor = corner[0]
                
                print(f'top_l = [{left_cor}, {top_cor}]\nbot_r = [{right_cor}, {bot_cor}]')

                top_l = np.array([left_cor, top_cor])
                bot_r = np.array([right_cor, bot_cor])
                print(f'corners to use: {top_l} and {bot_r}')
                height = bot_r[0] - top_l[0]
                length = bot_r[1] - top_l[1]
                print(f'size of tag = {height}, {length} px')
                edge_dist_y = np.ceil(height/4)
                edge_dist_x = np.ceil(length/4)

                # get the absolute edges of the grid at which the tag sits in
                grid_l = top_l[0] - edge_dist_y
                grid_r = bot_r[0] + edge_dist_y
                grid_t = top_l[1] - edge_dist_x
                grid_b = bot_r[1] + edge_dist_x
                if grid_b >= 480:
                    grid_b = 479
                if grid_r >= 640:
                    grid_r = 639
                if grid_l < 0:
                    grid_l = 0
                if grid_t < 0:
                    grid_t = 0
                grid_t_l = [int(grid_t), int(grid_l)]
                grid_b_r = [int(grid_b), int(grid_r)]

                print(f'the grid\'s [top, bottom, left and right] vals = [{grid_t}, {grid_b}, {grid_l}, {grid_r}]')

                if status == 1 :
                    print(f'colour blue from (y,x): grid {grid_t_l} to {grid_b_r}')
                    self.blue(grid_t_l, grid_b_r)

                elif status == 2 :
                    print(f'colour green from (y,x): grid {grid_t_l} to {grid_b_r}')
                    self.green(grid_t_l, grid_b_r)
                
                elif status == 3 :
                    print(f'colour red from (y,x): grid {grid_t_l} to {grid_b_r}')
                    self.red(grid_t_l, grid_b_r)
                
                else:
                    print('no colour')

                print('\n\n')
            marker_num += 1

        cv.imshow('vid_detected markers', self.img)
        cv.waitKey(0) 
        cv.destroyAllWindows()

    def blue(self, top_l, bot_r):
        for y in range(top_l[0],bot_r[0]):
            for x in range(top_l[1],bot_r[1]):
                colour = self.img[y,x]
                if colour[0] >= 215 :
                    self.img[y,x,1] -= 40
                    self.img[y,x,2] -= 40
                else:
                    self.img[y,x,0] += 40

    def green(self, top_l, bot_r):
        for y in range(top_l[0],bot_r[0]):
            for x in range(top_l[1],bot_r[1]):
                colour = self.img[y,x]
                if colour[1] >= 215 :
                    self.img[y,x,0] -= 40
                    self.img[y,x,2] -= 40
                else:
                    self.img[y,x,1] += 40

    def red(self, top_l, bot_r):
        for y in range(top_l[0],bot_r[0]):
            for x in range(top_l[1],bot_r[1]):
                colour = self.img[y,x]
                if colour[2] >= 215 :
                    self.img[y,x,0] -= 40
                    self.img[y,x,1] -= 40
                else:
                    self.img[y,x,2] += 40

#run the main code
edge_det()