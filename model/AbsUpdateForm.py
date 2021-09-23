import shutil
from tkinter import Tk, font, Label, StringVar, Entry, ttk, Canvas, Image, NW, Button, BooleanVar, Checkbutton, \
    DISABLED, filedialog

from PIL import Image
from PIL import ImageTk as itk

import DBAccessor


class AbsUpdateForm:
    def __init__(self, old_values, main):
        self.mainF = main
        self.old_values = old_values
        self.root = Tk()
        self.funny_font = font.Font(font='Arial', size=12)

        Label(self.root, text='Поле', font=self.funny_font).grid(row=0, column=0)
        Label(self.root, text='Текущее', font=self.funny_font).grid(row=0, column=1)
        Label(self.root, text='Новое', font=self.funny_font).grid(row=0, column=2)
        Label(self.root, text='ID', font=self.funny_font).grid(row=1, column=0)

        self.VarID = StringVar(self.root, str(old_values[0]))
        Label(self.root, text=str(old_values[0]), font=self.funny_font).grid(row=1, column=1)
        Entry(self.root, text=self.VarID, font=self.funny_font).grid(row=1, column=2)
        self.VarID.trace('w', self.scan_enabling)

        self.enter_button = Button(self.root, text='Изменить', state=DISABLED, font=self.funny_font, command=self.go)
        self.enter_button.grid(row=10, columnspan=3)

        self.root.mainloop()



    def change_photo(self):
        raise TypeError('Abstract Method')


    def scan_enabling(self, is_ok):
        raise TypeError('Abstract Method')

    def set_execute_button_state(self, value):
        if value:
            self.enter_button['state'] = 'normal'
        else:
            self.enter_button['state'] = 'disabled'

    def go(self):
        self.root.destroy()