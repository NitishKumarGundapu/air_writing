import cv2
from PIL import Image, ImageTk
from tkinter import *
from tkinter.ttk import *

root = Tk()
root.resizable(False,False)
root.geometry('600x600')
root.title('This is my Legacy')

def upload(z="i am lingaa"):
    print("i am also legend"+z)

z = "nice"

Button(root,text="Start",width=15,command= lambda :upload(z)).place(x=27,y=30)
Button(root,text="Stop",width=15,command= lambda :upload(z)).place(x=137,y=30)
Button(root,text="Undo",width=15,command= lambda :upload(z)).place(x=247,y=30)
Button(root,text="Redo",width=15,command= lambda :upload(z)).place(x=357,y=30)
Button(root,text="Photo",width=15,command= lambda :upload(z)).place(x=467,y=30)


panel = Label(root)
panel.pack(padx=10, pady=10)
vs = cv2.VideoCapture(0)

ok, frame = vs.read()
if ok: 
    cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA) 
    current_image = Image.fromarray(cv2image)  # convert image for PIL
    imgtk = ImageTk.PhotoImage(image=self.current_image)  # convert image for tkinter
    panel.imgtk = imgtk  # anchor imgtk so it does not be deleted by garbage-collector
    panel.config(image=imgtk)  # show the image
root.after(30, self.video_loop)

root.mainloop()