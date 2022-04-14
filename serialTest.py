import cv2
import math
import serial
import time

ser = serial.Serial("/dev/ttyACM0", 9600, timeout = 0.01)
ser.setDTR(False)
time.sleep(1)
ser.flushInput()
ser.setDTR(True)
time.sleep(2)

ser.write("x".encode())
time.sleep(0.5)
j = 0

while True:
    text = input("").strip()
    ser.write(text.encode())
    #time.sleep(0.5)
    j+= 1
    if j == 30:
        break
    
    