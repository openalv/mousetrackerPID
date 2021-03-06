import imutils
import threading
import cv2
import numpy as np
import argparse
from threading import Timer, Thread, Event
from random import *
from collections import deque


class perpetualTimer():

   def __init__(self,t,hFunction):
      self.t=t
      self.hFunction = hFunction
      self.thread = Timer(self.t,self.handle_function)

   def handle_function(self):
      self.hFunction()
      self.thread = Timer(self.t,self.handle_function)
      self.thread.start()

   def start(self):
      self.thread.start()

   def cancel(self):
      self.thread.cancel()


#random amplification
RAND = 15
#construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-b", "--buffer", type=int, default = 64)
args = vars(ap.parse_args())

#Constans
title= "Mouse Tracking with Kalman Filter"
height = 600
width = 800
grey = 150
colorMouse1 = (64, 255, 255)
colorMouse2 = (255, 64, 255)
traceMouse = deque(maxlen = args["buffer"])

mouse_measurement = 0,0


#Frame creation
frame = np.ones((height,width,3),np.uint8) * grey

def mouseMove(event, x, y, s, p):
    global mouse_measurement
    current_measurement = np.array([[np.float32(x)], [np.float32(y)]])
    mouse_measurement = current_measurement[0], current_measurement[1]
    #cv2.circle(frame, mouse_measurement, 1, colorMouse1, -1)

    return

def timeInterrupt():
    global frame
    pointMouseRandom = mouse_measurement[0] + randint(-RAND, RAND), mouse_measurement[1]+ randint(-RAND, RAND)
    frame = np.ones((height,width,3),np.uint8) * grey
    #cv2.circle(frame, pointmouse, 1, colormouse1, -1)
    cv2.circle(frame, pointMouseRandom, 6, colorMouse2, -1)
    traceMouse.appendleft(mouse_measurement)

   # loop over the set of tracked points
    for i in range(1, len(traceMouse)):
        # if either of the tracked points are None, ignore
	# them
        if traceMouse[i - 1] is None or traceMouse[i] is None:
            continue
	# otherwise, compute the thickness of the line and
	# draw the connecting lines
        thickness1 = int(np.sqrt(args["buffer"] / float(i + 1)) * 2.5)
        thickness2 = 1      
        cv2.line(frame, traceMouse[i - 1], traceMouse[i], (0, 0, 255), thickness1)
    return



cv2.namedWindow(title)
cv2.setMouseCallback(title, mouseMove)

# TODO : MAKE THE TIMER INTERRUPT WORKING
#t = threading.Timer(1, timeInterrupt)
#t.start()
timer = perpetualTimer(0.01,timeInterrupt)
timer.start()
while True:
 
    cv2.imshow(title,frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        timer.cancel()
        break

cv2.destroyAllWindows()
