from PIL import Image, ImageTk
from tkinter import messagebox as tk1
import tkinter as tk
import tkinter.ttk as ttk
import datetime
from collections import deque
import numpy as np
import cv2
import os

class Application:
    def __init__(self, output_path = "./"):
        self.undopoints=[]
        self.redopoints=[]
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

        self.paintWindow = np.zeros((480,640,3)) + 255
        self.paintWindow = cv2.rectangle(self.paintWindow, (15,5), (85,40), (0,0,0), 2)
        self.paintWindow = cv2.rectangle(self.paintWindow, (105,5), (175,40), (0,0,0), 2)
        self.paintWindow = cv2.rectangle(self.paintWindow, (195,5), (265,40), (0,0,0), 2)
        self.paintWindow = cv2.rectangle(self.paintWindow, (285,5), (355,40), self.colors[0], -1)
        self.paintWindow = cv2.rectangle(self.paintWindow, (375,5), (445,40), self.colors[1], -1)
        self.paintWindow = cv2.rectangle(self.paintWindow, (465,5), (532,40), self.colors[2], -1)
        self.paintWindow = cv2.rectangle(self.paintWindow, (550,5), (615,40), self.colors[3], -1)

        cv2.putText(self.paintWindow, "CLEAR", (28, 28), cv2.FONT_HERSHEY_SIMPLEX, 0.42, (0, 0, 0), 2, cv2.LINE_AA)
        cv2.putText(self.paintWindow, "UNDO", (118, 28), cv2.FONT_HERSHEY_SIMPLEX, 0.42, (0, 0, 0), 2, cv2.LINE_AA)
        cv2.putText(self.paintWindow, "REDO", (208, 28), cv2.FONT_HERSHEY_SIMPLEX, 0.42, (0, 0, 0), 2, cv2.LINE_AA)
        cv2.putText(self.paintWindow, "BLUE", (298, 28), cv2.FONT_HERSHEY_SIMPLEX, 0.42, (255, 255, 255), 2, cv2.LINE_AA)
        cv2.putText(self.paintWindow, "GREEN", (388, 28), cv2.FONT_HERSHEY_SIMPLEX, 0.42, (255, 255, 255), 2, cv2.LINE_AA)
        cv2.putText(self.paintWindow, "RED", (483, 28), cv2.FONT_HERSHEY_SIMPLEX, 0.42, (255, 255, 255), 2, cv2.LINE_AA)
        cv2.putText(self.paintWindow, "YELLOW", (557, 28), cv2.FONT_HERSHEY_SIMPLEX, 0.42, (150,150,150), 2, cv2.LINE_AA)
        
        self.output_path = output_path
        self.current_image = None
        self.screen_shot = cv2.imread('images\\white_image.jpg')
        self.screen_shot = cv2.resize(self.screen_shot , (640,480))
        self.undo_array = []
        self.redo_array = []

        self.root = tk.Tk()
        self.root.title("Computer Vision Writing")
        self.root.protocol('WM_DELETE_WINDOW', self.destroy)

        self.panel = ttk.Label(self.root)
        self.panel.pack(padx=10, pady=10)

        btn = ttk.Button(self.root, text="Screenshot", command=self.take_snapshot)
        btn1 = ttk.Button(self.root, text="Start", command=self.video_loop)
        btn2 = ttk.Button(self.root, text="Help", command= self.help_desk)
        btn5 = ttk.Button(self.root, text="Quit", command=self.destroy)
        
        btn1.pack(side = "left", expand = True, fill = "both")
        btn.pack(side = "left", expand = True, fill = "both")
        btn2.pack(side = "left", expand = True, fill = "both")
        btn5.pack(side = "left", expand = True, fill = "both")

        cv2image = cv2.imread('images\\nice.jpg')
        self.current_image = Image.fromarray(cv2image)
        imgtk = ImageTk.PhotoImage(image=self.current_image)
        self.panel.imgtk = imgtk
        self.panel.config(image=imgtk)
        self.vs = cv2.VideoCapture(0,cv2.CAP_DSHOW)


    def video_loop(self):

        ok, frame = self.vs.read()
        frame = cv2.flip(frame, 1)
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        Upper_hsv = np.array([153,255,255])
        Lower_hsv = np.array([64,72,49])

        frame = cv2.rectangle(frame, (15,5), (85,40), (0,0,0), 2)
        frame = cv2.rectangle(frame, (105,5), (175,40), (0,0,0), 2)
        frame = cv2.rectangle(frame, (195,5), (265,40), (0,0,0), 2)
        frame = cv2.rectangle(frame, (285,5), (355,40), self.colors[0], -1)
        frame = cv2.rectangle(frame, (375,5), (445,40), self.colors[1], -1)
        frame = cv2.rectangle(frame, (465,5), (535,40), self.colors[2], -1)
        frame = cv2.rectangle(frame, (550,5), (615,40), self.colors[3], -1)

        cv2.putText(frame, "CLEAR", (28, 28), cv2.FONT_HERSHEY_SIMPLEX, 0.42, (0, 0, 0), 2, cv2.LINE_AA)
        cv2.putText(frame, "UNDO", (118, 28), cv2.FONT_HERSHEY_SIMPLEX, 0.42, (0, 0, 0), 2, cv2.LINE_AA)
        cv2.putText(frame, "REDO", (208, 28), cv2.FONT_HERSHEY_SIMPLEX, 0.42, (0, 0, 0), 2, cv2.LINE_AA)
        cv2.putText(frame, "BLUE", (298, 28), cv2.FONT_HERSHEY_SIMPLEX, 0.42, (255, 255, 255), 2, cv2.LINE_AA)
        cv2.putText(frame, "GREEN", (388, 28), cv2.FONT_HERSHEY_SIMPLEX, 0.42, (255, 255, 255), 2, cv2.LINE_AA)
        cv2.putText(frame, "RED", (483, 28), cv2.FONT_HERSHEY_SIMPLEX, 0.42, (255, 255, 255), 2, cv2.LINE_AA)
        cv2.putText(frame, "YELLOW", (557, 28), cv2.FONT_HERSHEY_SIMPLEX, 0.42, (150,150,150), 2, cv2.LINE_AA)

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

            if center[1] <= 40:
                if 105<= center[0] <=175: #undo
                    if len(self.undopoints)>0:
                        nice=self.undopoints.pop()
                        self.redopoints.append(nice)
                        if nice[1]==0:
                            if len(self.bpoints[nice[-1]])>0:
                                    self.bpoints[nice[-1]].popleft()
                        elif nice[1]==1:
                            if len(self.gpoints[nice[-1]])>0:
                                    self.gpoints[nice[-1]].popleft()
                        elif nice[1]==2:
                            if len(self.rpoints[nice[-1]])>0:
                                    self.rpoints[nice[-1]].popleft()
                        elif nice[1]==3:
                            if len(self.ypoints[nice[-1]])>0:
                                    self.ypoints[nice[-1]].popleft()

                elif 195<=center[0]<=265: #redo
                    try:
                        nice2=self.redopoints.pop()
                        self.undopoints.append(nice2)
                        if nice2[1]==0:
                            self.bpoints[nice2[-1]].appendleft(nice2[0])
                        elif nice2[1]==1:
                            self.gpoints[nice2[-1]].appendleft(nice2[0])
                        elif nice2[1]==2:
                            self.rpoints[nice2[-1]].appendleft(nice2[0])
                        elif nice2[1]==3:
                            self.ypoints[nice2[-1]].appendleft(nice2[0])
                    except:
                        pass

                if 15 <= center[0] <= 85: #clear button     
                    self.undo_array.append(self.screen_shot)
                    self.bpoints = [deque(maxlen=512)]
                    self.gpoints = [deque(maxlen=512)]
                    self.rpoints = [deque(maxlen=512)]
                    self.ypoints = [deque(maxlen=512)]

                    self.undopoints=[]
                    self.redopoints=[]
                    self.blue_index = 0
                    self.green_index = 0
                    self.red_index = 0
                    self.yellow_index = 0

                    self.paintWindow[67:,:,:] = 255
                    self.undo_array.append(self.screen_shot)
                    self.screen_shot[:,:,:] = 255

                elif 285 <= center[0] <= 355:
                    self.colorIndex = 0
                elif 375 <= center[0] <= 445:
                    self.colorIndex = 1
                elif 465 <= center[0] <= 535:
                    self.colorIndex = 2
                elif 550 <= center[0] <= 615:
                    self.colorIndex = 3
            else:
                if self.colorIndex == 0:
                    self.bpoints[self.blue_index].appendleft(center)
                    self.undopoints.append([center,self.colorIndex,self.blue_index])
                elif self.colorIndex == 1:
                    self.gpoints[self.green_index].appendleft(center)
                    self.undopoints.append([center,self.colorIndex,self.green_index])
                elif self.colorIndex == 2:
                    self.rpoints[self.red_index].appendleft(center)
                    self.undopoints.append([center,self.colorIndex,self.red_index])
                elif self.colorIndex == 3:
                    self.ypoints[self.yellow_index].appendleft(center)
                    self.undopoints.append([center,self.colorIndex,self.yellow_index])
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
                        cv2.line(self.screen_shot, points[i][j][k - 1], points[i][j][k], self.colors[i], 2)

        cv2.imshow("Tracking", frame)
        cv2.imshow("Paint", self.paintWindow)
        cv2.imshow("mask",Mask)

        cv2image = cv2.cvtColor(self.screen_shot, cv2.COLOR_BGR2RGBA)
        self.current_image = Image.fromarray(cv2image)
        imgtk = ImageTk.PhotoImage(image=self.current_image)
        self.panel.imgtk = imgtk
        self.panel.config(image=imgtk)

        self.root.after(10, self.video_loop)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            self.destroy()

    def take_snapshot(self):
        ts = datetime.datetime.now()
        filename = "{}.jpg".format(ts.strftime("%Y-%m-%d_%H-%M-%S"))
        p = os.path.join(self.output_path, filename)
        k = self.current_image.convert('RGB')
        k.save(p, "JPEG")
        print("[INFO] saved {}".format(filename))
        tk1.showinfo("Sucessful","Screenshot saved Sucessfully")

    def setValues(self,x):
        print("",end="")
    
    def help_desk(self):
        rooth = tk.Tk()
        rooth.resizable(False,False)
        rooth.geometry('400x450')
        rooth.title('Help Desk')
        ttk.Label(rooth,text = "Instructions",width=20,font=("Consolas",17)).place(x=120,y=20)
        ttk.Label(rooth,text='1 . Click on the start button to start the \n CV writing.',font=("Consolas",10)).place(x=20,y=80)
        ttk.Label(rooth,text='2 . Select different colors according to your \n preference and start writing.',font=("Consolas",10)).place(x=20,y=130)
        ttk.Label(rooth,text='3 . Click on Undo or redo button to undo or redo \n your work on the screen',font=("Consolas",10)).place(x=20,y=180)
        ttk.Label(rooth,text="4 . click on clear all to clear all your work \npresent on the screen",font=("Consolas",10)).place(x=20,y=230)
        ttk.Label(rooth,text="5 . You can take a screenshot of your work\n if necessary.",font=("Consolas",10)).place(x=20,y=280)
        ttk.Label(rooth,text="6 . For further details contact \n   1 . 18311A0554@sreenidhi.edu.in  \n   2 . 18311A0519@sreenidhi.edu.in  \n   3 . 18311A0532@sreenidhi.edu.in  \n",font=("Consolas",10)).place(x=20,y=330)

        rooth.mainloop()

    def destroy(self):
        cv2.destroyAllWindows()
        self.vs.release()
        self.root.destroy()


pba = Application('images\\screenshots\\')
pba.root.mainloop()