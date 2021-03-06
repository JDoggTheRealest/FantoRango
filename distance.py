import cv2
import math
import serial
import time

# ser = serial.Serial("/dev/ttyAM0", 115200, timeout = 1)
# ser.setDTR(False)
# time.sleep(1)
# ser.flushInput()
# ser.setDTR(True)
# time.sleep(2)

distance = 0.0
font = cv2.FONT_HERSHEY_SIMPLEX
# Capture from the default deivce
cap = cv2.VideoCapture(0)
# The samples thingy
# Make sure the file is in the same folder as the program..
# otherwise this will not work
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier('haarcascade_eye.xml')
while True:
    start = time.time()
    # Caputure a single frame
    ret, huge_frame = cap.read()
    
    frame = cv2.resize(huge_frame, (0,0), fx=0.7, fy=0.7, interpolation=cv2.INTER_NEAREST)
#Create the greyscale and detect faces
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    # Add squeres for each face
    
    for (x, y, w, h) in faces:
        distancei = (100*49)/w#2.54*(2*3.14 * 180)/(w+h*360)*1000 + 3
        #print distancei
#        distance = distancei *2.54
        distance = math.floor(distancei)
        #if ((x + w/2 - 577))
        print(w,h)
        cv2.rectangle(frame, (x,y), (x+w,y+h), (255,0,0), 2)
#         roi_gray = gray[y:y+h, x:x+w]
#         roi_color = frame[y:y+h, x:x+w]
#         eyes = eye_cascade.detectMultiScale(roi_gray)
#         for (ex,ey,ew,eh) in eyes:
#             cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(0,255,0),2)

    # Display the resulting frame
    cv2.putText(frame,'Distance = ' + str(distance) + ' cm', (5,100),font,1,(255,255,255),2)
    cv2.imshow('face detection', frame)
    cv2.waitKey(1)
    print(1/(time.time() - start))
    #if cv2.waitKey(1) == ord('q'):
     #   break
 
 
# Stop the capture
cap.release()
# Destory the window
cv2.destroyAllWindows()
