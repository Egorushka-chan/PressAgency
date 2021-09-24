from tkinter import *
from tkinter import font

from PIL import Image
from PIL import ImageTk as itk

import DBAccessor



class AboutFrom:
    def __init__(self):
        self.root = Tk()
        self.root.title('О программе Press Agency')

        self.largeFont = font.Font(size=14)
        self.smallFont = font.Font(size=11)

        self.iconCanvas = Canvas(self.root, width=96, height=96)
        self.iconCanvas.grid(column=0, row=0, rowspan=2, padx=10, pady=10)
        img = Image.open(DBAccessor.base_path + r"photos/program/pressIcon.png")
        imgItk = itk.PhotoImage(img, master=self.root)
        self.iconCanvas.image = imgItk
        self.iconCanvas.create_image(0, 0, anchor=NW, image=imgItk)

        Label(self.root, text='Press Agency 0.9.9 (Scholar Edition)', font=self.largeFont).grid(row=0, column=1)
        Label(self.root, text='Build #PC-0.9001Develop, build in September 24, 2021', font=self.smallFont).grid(row=1,column=1)

        Label(self.root, text='Powered by Python', font=self.smallFont).grid(row=2, column=1, pady=10, sticky='w')
        Label(self.root, text='Bla Bla Bla (Something Very Smart)', font=self.smallFont).grid(row=3,column=1, sticky='w')

        Label(self.root, text='No Copyright (c)', font=self.smallFont).grid(row=4,column=1,pady=10, sticky='w')
        self.root.mainloop()


if __name__ == '__main__':
    AboutFrom()
