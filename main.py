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

root.mainloop()