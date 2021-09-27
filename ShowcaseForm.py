from tkinter import *
from tkinter import messagebox
import os
from PIL import Image
from PIL import ImageTk as itk


import DBAccessor


class Showcase:
    def __init__(self):
        self.root = Tk()
        self.root.title('Витрина')

        self.editions = DBAccessor.select_info(fr0m='Edition')
        # self.photos_path = [path for path in os.listdir(DBAccessor.base_path + r"photos/editions/") if
        #                     path != 'none.png']

        self.currentFrame = 0
        self.frameList = []

        self.photo_fill()
        self.root.mainloop()

    def photo_fill(self):
        monitor_width = self.root.winfo_screenwidth()
        monitor_height = self.root.winfo_screenheight()
        current_height = 0
        max_height = 0
        current_len = 0
        for edition in self.editions:
            if self.currentFrame == len(self.frameList):
                frame = Frame(self.root)
                frame.grid(row=self.currentFrame, column=0)
                self.frameList.append(frame)

            img = Image.open(
                DBAccessor.base_path + r"photos/editions/" + edition[3] if edition[3] != ''
                                                                           or edition[3] is not None else 'none.png')
            width, height = img.size
            while width > 300 or height > 300:
                width, height = width / 2, height / 2

            if height > max_height:
                max_height = height

            photo_frame = Frame(self.frameList[self.currentFrame])
            new_canvas = Canvas(photo_frame, width=width, height=height)
            new_canvas.pack()
            Label(photo_frame, text=f'{edition[1]} - {edition[2]} руб.').pack()
            photo_frame.pack(padx=5, side='left')

            img.thumbnail((width, height), Image.ANTIALIAS)
            imgNew = itk.PhotoImage(img, master=self.frameList[self.currentFrame])
            new_canvas.image = imgNew
            new_canvas.create_image(0, 0, anchor=NW, image=imgNew)

            current_len += width

            new_canvas.bind("<Button-1>", lambda t1=None, t2=None, t3=None, edition=edition: self.canvas_click(edition))

            if current_len + 400 > monitor_width:
                self.currentFrame += 1
                current_len = 0
                current_height += max_height
                max_height = 0

            if current_height > monitor_height - 200:
                return

    def canvas_click(self, edition):
       messagebox.showinfo('Издание', f'ID - {edition[0]}; Название - {edition[1]}; Цена - {edition[2]}; Фото - {edition[3]}', master=self.root)

