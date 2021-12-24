from PIL import Image, ImageTk
import tkinter as tk
import argparse
import datetime
import cv2
import os

class Application:
     def __init__(self, output_path = "./"):
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
          #cv2image = cv2.resize(cv2image, (350, 150))
          self.current_image = Image.fromarray(cv2image)
          imgtk = ImageTk.PhotoImage(image=self.current_image)
          self.panel.imgtk = imgtk
          self.panel.config(image=imgtk)
          self.vs = cv2.VideoCapture(0,cv2.CAP_DSHOW)
          
     def video_loop(self):
          ok, frame = self.vs.read()
          if ok:
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
          self.current_image.save(p, "JPEG")
          #print("[INFO] saved {}".format(filename))

     def destructor(self):
          self.root.destroy()
          self.vs.release()
          cv2.destroyAllWindows()

     def setValues(self):
          print("")

ap = argparse.ArgumentParser()
ap.add_argument("-o", "--output", default="./",
    help="path to output directory to store snapshots (default: current folder")
args = vars(ap.parse_args())

pba = Application(args["output"])
pba.root.mainloop()