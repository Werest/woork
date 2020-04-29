from tkinter import *

root = Tk()

root.title('Автоматическая детекция')
root.geometry('1280x720')
root.resizable(width=False, height=False)

l = Label(text='Порог', font='13')
l1 = Label(text='Размер', font='13')

var = DoubleVar()
scale = Scale(root, variable=var, length=400, orient=HORIZONTAL, from_=0, to=.99, tickinterval=0.01, resolution=0.01)
scale.pack()

scale1 = Scale(root, variable=var, length=400, orient=HORIZONTAL, from_=0, to=.99, tickinterval=0.01, resolution=0.01)
scale1.pack()

l.pack()
scale.pack()
l1.pack()
scale1.pack()

root.mainloop()
