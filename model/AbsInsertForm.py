from tkinter import *
from tkinter import ttk, font, filedialog


class AbsInsertForm:
    def __init__(self, main):
        self.mainF = main
        self.root = Tk()
        self.funny_font = font.Font(font='Arial', size=12)

        self.enter_button = Button(self.root, text='EXECUTE', state=DISABLED, font=self.funny_font, command=self.go)
        self.enter_button.grid(row=10, columnspan=2)
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def scan_enability(self):
        raise TypeError('Abstract Method')

    def go(self):
        raise TypeError('Abstract Method')

    def on_closing(self):
        self.mainF.info_fill()
        self.root.destroy()
