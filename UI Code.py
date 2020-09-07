from tkinter import *

#tkinter.Tk(sreenName=None, baseName=None, className='Tk', useTk=1)

window=Tk()

btn=Button(window, text="Test Button", fg="blue")
btn.place(x=80, y=100)

window.title("Test")
window.geometry("300x200+10+20")
window.mainloop()
