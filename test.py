import cv2
import math
import serial
import time
distance = 0.0

#Serial stuff
# ser = serial.Serial("/dev/ttyACM0", 115200, timeout = 1)
# ser.setDTR(False)
# time.sleep(1)
# ser.flushInput()
# ser.setDTR(True)
# time.sleep(2)

cap = cv2.VideoCapture(0)
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
#eye_cascade = cv2.CascadeClassifier('haarcascade_eye.xml')


ret, huge_frame = cap.read()

# edvard = 0
scale = 0.5
d = 2
midX = int(scale*640/(2*d))
midY = int(scale*480/(2*d))
print(midX, midY)
width = int(midX/2)
height = int(midY/2)

def findFace(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    return faces

def drawImageWithFaceBox(frame, n, m):
    distance = 0.0
    faces = findFace(frame[midY*m:midY*(m+2) ,midX*n:midX*(n+2)])
    for (x, y, w, h) in faces:
        distancei = (100*49)/w#2.54*(2*3.14 * 180)/(w+h*360)*1000 + 3
        distance = math.floor(distancei)
        cv2.rectangle(frame, (x + n*midX, y + m*midY), (x + w + n*midX,y + h + m*midY), (255,0,0), 2)
        print(x + 2*n*midX, y + 2*m*midY)
        
#         if(x + n*midX < midX):
#             ser.write("x\n".encode())
#         else:
#             ser.write("y\n".encode())
    #cv2.putText(frame,'Distance = ' + str(distance) + ' cm', (5,100),font,1,(255,255,255),2)
    cv2.imshow('face detection', frame)
   # cv2.imshow("face detection", huge_frame[midY*m:midY*(m+1) ,midX*n:midX*(n+1)])
    cv2.waitKey(1)    

n = 0
m = 0
drawImageWithFaceBox(huge_frame, 0, 0)
while True:
    start = time.time()
    ret, huge_frame = cap.read()
    frame = cv2.resize(huge_frame, (0,0), fx=scale, fy=scale, interpolation=cv2.INTER_NEAREST)
    drawImageWithFaceBox(frame, n, m)
    n+=1
    if(n==2*d - 1):
        n = 0
        m+=1
        if(m==2*d - 1):
            m = 0
    print(1/(time.time() - start))
#     if(n==0):
#         drawImageWithFaceBox(huge_frame[midY - height: midY + height ,midX - width:midX + width])
#     elif(n==1):
#         drawImageWithFaceBox(huge_frame[0:midY, 0:midX])
#     elif(n==2):
#         drawImageWithFaceBox(huge_frame[0:midY, midX:])
#     elif(n==3):
#         drawImageWithFaceBox(huge_frame[midY:, 0:midX])
#     else:
#         drawImageWithFaceBox(huge_frame[midY:, midX:])
#         n=-1
    #n+=1



# while True:
#     # Caputure a single frame
#     ret, huge_frame = cap.read()
#     frame = cv2.resize(huge_frame, (0,0), fx=1, fy=1, interpolation=cv2.INTER_NEAREST)
# # Create the greyscale and detect faces
#     gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
#     test = gray[X-width:X+width, Y-height:Y+height]
#     if(edvard%1 == 0):
#         faces = face_cascade.detectMultiScale(huge_frame, 1.3, 5)
#     # Add squeres for each face
# #         for (x, y, w, h) in faces:
# #             distancei = 2.54*(2*3.14 * 180)/(w+h*360)*1000 + 3
# #         #print distancei
# # #        distance = distancei *2.54
# #             distance = math.floor(distancei/2)
# #             cv2.rectangle(frame, (x,y), (x+w,y+h), (255,0,0), 2)
# #             roi_gray = gray[y:y+h, x:x+w]
# #             print(roi_gray)
# #             roi_color = frame[y:y+h, x:x+w]
# #             print(x)
#         #cv2.putText(frame,'Distance = ' + str(distance) + ' cm', (5,100),font,1,(255,255,255),2)
#         cv2.imshow('face detection',  frame)
#     
#             #eyes = eye_cascade.detectMultiScale(roi_gray)
#             #for (ex,ey,ew,eh) in eyes:
#             #    cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(0,255,0),2)
#     #cv2.imshow('face detection', frame)
#     # Display the resulting frame
#     edvard+=1
#     if cv2.waitKey(10) == ord('q'):
#         break
#  
#  
# # Stop the capture
# cap.release()
# # Destory the window
# cv2.destroyAllWindows()
# 
