import cv2
import math
import time

cap = cv2.VideoCapture(0)

while True:
    start = time.time()
    ret, huge_frame = cap.read()
    #frame = cv2.resize(huge_frame, (0,0), fx=1, fy=0.4, interpolation=cv2.INTER_NEAREST)
    #cv2.imshow('face detection', huge_frame)
    print(1/(time.time() - start))
    cv2.waitKey(1)    
     
