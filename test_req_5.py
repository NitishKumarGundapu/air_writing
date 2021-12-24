from PIL import Image, ImageTk
import tkinter as tk
import argparse
import datetime
from collections import *
import numpy as np
import cv2
import os

class Application:
     def __init__(self, output_path = "./"):
          cv2.namedWindow("Color detectors")
          cv2.createTrackbar("Upper Hue", "Color detectors", 153, 180,self.setValues)
          cv2.createTrackbar("Upper Saturation", "Color detectors", 255, 255,self.setValues)
          cv2.createTrackbar("Upper Value", "Color detectors", 255, 255,self.setValues)
          cv2.createTrackbar("Lower Hue", "Color detectors", 64, 180,self.setValues)
          cv2.createTrackbar("Lower Saturation", "Color detectors", 72, 255,self.setValues)
          cv2.createTrackbar("Lower Value", "Color detectors", 49, 255,self.setValues)

          self.bpoints = [deque(maxlen=1024)]
          self.gpoints = [deque(maxlen=1024)]
          self.rpoints = [deque(maxlen=1024)]
          self.ypoints = [deque(maxlen=1024)]

          self.blue_index = 0
          self.green_index = 0
          self.red_index = 0
          self.yellow_index = 0
          self.kernel = np.ones((5,5),np.uint8)
          self.colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (0, 255, 255)]
          self.colorIndex = 0

          self.paintWindow = np.zeros((471,636,3)) + 255
          self.paintWindow = cv2.rectangle(self.paintWindow, (40,1), (140,65), (0,0,0), 2)
          self.paintWindow = cv2.rectangle(self.paintWindow, (160,1), (255,65), self.colors[0], -1)
          self.paintWindow = cv2.rectangle(self.paintWindow, (275,1), (370,65), self.colors[1], -1)
          self.paintWindow = cv2.rectangle(self.paintWindow, (390,1), (485,65), self.colors[2], -1)
          self.paintWindow = cv2.rectangle(self.paintWindow, (505,1), (600,65), self.colors[3], -1)

          cv2.putText(self.paintWindow, "CLEAR", (49, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2, cv2.LINE_AA)
          cv2.putText(self.paintWindow, "BLUE", (185, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
          cv2.putText(self.paintWindow, "GREEN", (298, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
          cv2.putText(self.paintWindow, "RED", (420, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
          cv2.putText(self.paintWindow, "YELLOW", (520, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (150,150,150), 2, cv2.LINE_AA)
          
          self.output_path = output_path
          self.current_image = None

          self.root = tk.Tk()
          self.root.title("Air Writing")
          self.root.protocol('WM_DELETE_WINDOW', self.destructor)

          self.panel = tk.Label(self.root)
          self.panel.pack(padx=10, pady=10)

          btn = tk.Button(self.root, text="Snapshot!", command=self.take_snapshot)
          btn1 = tk.Button(self.root, text="Start", command=self.video_loop)
          btn2 = tk.Button(self.root, text="Exit", command=self.destructor)
          btn3 = tk.Button(self.root, text="Undo", command=self.destructor)
          btn4 = tk.Button(self.root, text="Redo", command=self.destructor)
          
          btn1.pack(side = "left", expand = True, fill = "both")
          btn.pack(side = "left", expand = True, fill = "both")
          btn2.pack(side = "left", expand = True, fill = "both")
          btn3.pack(side = "left", expand = True, fill = "both")
          btn4.pack(side = "left", expand = True, fill = "both")

          cv2image = cv2.imread('nice.jpg')
          self.current_image = Image.fromarray(cv2image)
          imgtk = ImageTk.PhotoImage(image=self.current_image)
          self.panel.imgtk = imgtk
          self.panel.config(image=imgtk)
          self.vs = cv2.VideoCapture(0,cv2.CAP_DSHOW)


     def video_loop(self):

          ok, frame = self.vs.read()

          frame = cv2.flip(frame, 1)
          hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

          u_hue = cv2.getTrackbarPos("Upper Hue", "Color detectors")
          u_saturation = cv2.getTrackbarPos("Upper Saturation", "Color detectors")
          u_value = cv2.getTrackbarPos("Upper Value", "Color detectors")
          l_hue = cv2.getTrackbarPos("Lower Hue", "Color detectors")
          l_saturation = cv2.getTrackbarPos("Lower Saturation", "Color detectors")
          l_value = cv2.getTrackbarPos("Lower Value", "Color detectors")
          Upper_hsv = np.array([u_hue,u_saturation,u_value])
          Lower_hsv = np.array([l_hue,l_saturation,l_value])

          frame = cv2.rectangle(frame, (40,1), (140,65), (122,122,122), -1)
          frame = cv2.rectangle(frame, (160,1), (255,65), self.colors[0], -1)
          frame = cv2.rectangle(frame, (275,1), (370,65), self.colors[1], -1)
          frame = cv2.rectangle(frame, (390,1), (485,65), self.colors[2], -1)
          frame = cv2.rectangle(frame, (505,1), (600,65), self.colors[3], -1)
          cv2.putText(frame, "CLEAR ALL", (49, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
          cv2.putText(frame, "BLUE", (185, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
          cv2.putText(frame, "GREEN", (298, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
          cv2.putText(frame, "RED", (420, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
          cv2.putText(frame, "YELLOW", (520, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (150,150,150), 2, cv2.LINE_AA)

          Mask = cv2.inRange(hsv, Lower_hsv, Upper_hsv)
          Mask = cv2.erode(Mask, self.kernel, iterations=1)
          Mask = cv2.morphologyEx(Mask, cv2.MORPH_OPEN, self.kernel)
          Mask = cv2.dilate(Mask, self.kernel, iterations=1)

          cnts,_ = cv2.findContours(Mask.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
          center = None

          if len(cnts) > 0: 
               cnt = sorted(cnts, key = cv2.contourArea, reverse = True)[0]
               ((x, y), radius) = cv2.minEnclosingCircle(cnt)
               cv2.circle(frame, (int(x), int(y)), int(radius), (0, 255, 255), 2)
               M = cv2.moments(cnt)
               center = (int(M['m10'] / M['m00']), int(M['m01'] / M['m00']))

               if center[1] <= 65:
                    if 40 <= center[0] <= 140:
                         self.bpoints = [deque(maxlen=512)]
                         self.gpoints = [deque(maxlen=512)]
                         self.rpoints = [deque(maxlen=512)]
                         self.ypoints = [deque(maxlen=512)]

                         self.blue_index = 0
                         self.green_index = 0
                         self.red_index = 0
                         self.yellow_index = 0

                         self.self.paintWindow[67:,:,:] = 255
                    elif 160 <= center[0] <= 255:
                         self.colorIndex = 0
                    elif 275 <= center[0] <= 370:
                         self.colorIndex = 1
                    elif 390 <= center[0] <= 485:
                         self.colorIndex = 2
                    elif 505 <= center[0] <= 600:
                         self.colorIndex = 3
               else :
                    if self.colorIndex == 0:
                         self.bpoints[self.blue_index].appendleft(center)
                    elif self.colorIndex == 1:
                         self.gpoints[self.green_index].appendleft(center)
                    elif self.colorIndex == 2:
                         self.rpoints[self.red_index].appendleft(center)
                    elif self.colorIndex == 3:
                         self.ypoints[self.yellow_index].appendleft(center)
          else:
               self.bpoints.append(deque(maxlen=512))
               self.blue_index += 1
               self.gpoints.append(deque(maxlen=512))
               self.green_index += 1
               self.rpoints.append(deque(maxlen=512))
               self.red_index += 1
               self.ypoints.append(deque(maxlen=512))
               self.yellow_index += 1

          points = [self.bpoints, self.gpoints, self.rpoints, self.ypoints]
          for i in range(len(points)):
               for j in range(len(points[i])):
                    for k in range(1, len(points[i][j])):
                         if points[i][j][k - 1] is None or points[i][j][k] is None:
                              continue
                         cv2.line(frame, points[i][j][k - 1], points[i][j][k], self.colors[i], 2)
                         cv2.line(self.paintWindow, points[i][j][k - 1], points[i][j][k], self.colors[i], 2)
               
          cv2.imshow("Tracking", frame)
          cv2.imshow("Paint", self.paintWindow)
          cv2.imshow("mask",Mask)
         
          cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
          self.current_image = Image.fromarray(cv2image)
          imgtk = ImageTk.PhotoImage(image=self.current_image)
          self.panel.imgtk = imgtk
          self.panel.config(image=imgtk)

          self.root.after(10, self.video_loop)

     def take_snapshot(self):
          ts = datetime.datetime.now()
          filename = "{}.jpg".format(ts.strftime("%Y-%m-%d_%H-%M-%S"))
          p = os.path.join(self.output_path, filename)
          k = self.current_image.convert('RGB')
          k.save(p, "JPEG")
          print("[INFO] saved {}".format(filename))

     def destructor(self):
          self.root.destroy()
          self.vs.release()
          cv2.destroyAllWindows()

     def setValues(self,x):
          print("",end="")

ap = argparse.ArgumentParser()
ap.add_argument("-o", "--output", default="./",
    help="path to output directory to store snapshots (default: current folder")
args = vars(ap.parse_args())

pba = Application(args["output"])
pba.root.mainloop()