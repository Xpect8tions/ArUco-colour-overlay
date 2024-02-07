import cv2 as cv
import numpy as np 


size = [160,160,3]
mask = np.zeros((size),np.uint8)
list_np = [[13,125],[115,12],[148,114],[125,155],[110,133]]
np_list = np.array(list_np,dtype=np.uint32)
cv.fillPoly(mask, [np_list.astype(int)], color=(255, 255, 255))
print(mask)
cv.imshow('mask',mask)
cv.waitKey(0)
