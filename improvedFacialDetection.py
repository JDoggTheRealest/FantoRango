import cv2
import math
import serial
import time

#Serial stuff
ser = serial.Serial("/dev/ttyACM0", 115200, timeout = 1)
ser.setDTR(False)
time.sleep(1)
ser.flushInput()
ser.setDTR(True)
time.sleep(2)

#Start videofeed and load CascadeClassifiers
cap = cv2.VideoCapture(0)
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
#eye_cascade = cv2.CascadeClassifier('haarcascade_eye.xml')

font = cv2.FONT_HERSHEY_SIMPLEX

#Parameters for program
scale = 0.7
d = 2
padX = 50
padY = 20

#Initialization of variabels
distance = 0.0
lastX = 0
lastY = 0
lastW = 0
lastH = 0
seen = False

#Temporary?
midX = int(scale*640/(2*d))
midY = int(scale*480/(2*d))

#n is index for frame in x-direction, while m is in y-direction
n = 0
m = 0
    
def trackingMethod(frame):
    frameX = int(lastX - padX) if lastX - padX > 0 else 0
    frameY = int(lastY - padY) if lastY - padY > 0 else 0
    return frame[frameY:frameY + lastH + 2*padY, frameX:frameX + lastW + 2*padX], frameX, frameY
 
def searchMethod(frame):
    global n
    global m
    
    frame = frame[midY*m:midY*(m+2) ,midX*n:midX*(n+2)]
    frameX = midX*n
    frameY = midY*m
    n+=1
    if(n==2*d - 1):
        n = 0
        m+=1
        if(m==2*d - 1):
            m = 0

    return frame, frameX, frameY

def findFace(frame, frameX, frameY):
    global distance
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    for (x, y, w, h) in faces:
        distance = math.floor((3.04*142*640*scale)/(w*3.68))#2.54*(2*3.14 * 180)/(w+h*360)*1000 + 3
        cv2.rectangle(reframe, (x + frameX, y + frameY), (x + w + frameX,y + h + frameY), (255,0,0), 2)
        return x + frameX, y + frameY, w, h, distance, True
    return 0, 0, 0, 0, 0, False
    #return lastX, lastY, lastW, lastH, distance, seen

pressed = False

def click(event, x, y, flags, param):
    global pressed
    if event == cv2.EVENT_LBUTTONDOWN:
        pressed = True
    else:
        pressed = False
        
cv2.namedWindow('face detection', cv2.WND_PROP_FULLSCREEN)
cv2.setWindowProperty('face detection', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
cv2.setMouseCallback('face detection', click)  
    
while True:
    #start = time.time()
    
    #Get frame
    ret, huge_frame = cap.read()
    #Resize frame to scale 0-1 using interpolation
    reframe = cv2.resize(huge_frame, (0,0), fx=scale, fy=scale, interpolation=cv2.INTER_NEAREST)
    
    if(seen):
        frame, frameX, frameY = trackingMethod(reframe)
    else:
        frame, frameX, frameY = searchMethod(reframe)
     
    lastX, lastY, lastW, lastH, distance, seen = findFace(frame, frameX, frameY)
    
    #Serial stuff
    #print(1/(time.time() - start))
    if(seen):
        #print(f"x{lastX + lastW/2 - 2*midX},y{lastY + lastH/2 - 2*midY},z{distance},{pressed}") 
        ser.write(f"{142*(lastX + lastW/2 - 2*midX)/lastW},{142*(lastY + lastH/2 - 2*midY)/lastW},{distance},{pressed}\n".encode())   
        #cv2.putText(reframe, f"{142*(lastX + lastW/2 - 2*midX)/lastW:.2f},{142*(lastY + lastH/2 - 2*midY)/lastW:.2f},{distance:.2f},{pressed}\n", (5,100),font,1,(255,255,255),2)
    
        #print(ser.readline().decode('utf-8').rstrip())
        #if(lastX + lastW/2 < 2*midX):
        #    ser.write("x\n".encode())
        #else:
        #    ser.write("y\n".encode())
    #cv2.imshow('face detection', reframe)
    
    if cv2.waitKey(1) == ord('q'):
        break
 
# Stop the capture
cap.release()
# Destory the window
cv2.destroyAllWindows()