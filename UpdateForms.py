import shutil
from tkinter import ttk, font, filedialog
from tkinter import *
from model.AbsUpdateForm import AbsUpdateForm
import DBAccessor
from PIL import Image
from PIL import ImageTk as itk
from model.TableEnum import Table


class ReadingUpdateForm(AbsUpdateForm):
    def __init__(self, old_values, main):
        super().__init__(old_values, main)
        Label(self.root, text='Подписчик', font=self.funny_font).grid(row=2, column=0)
        Label(self.root, text=str(self.old_values[1]), font=self.funny_font).grid(row=2, column=1)
        read_subs = DBAccessor.select_info(fr0m='Subscriber d JOIN Readings ON d.ID = Readings.ID_Subscriber',
                                           select='SELECT d.ID, d.Name, d.Surname')
        self.RSubCombo = ttk.Combobox(self.root, values=read_subs)
        self.RSubCombo.bind('<<ComboboxSelected>>', lambda e: self.combo_change('Sub'))
        self.RSubCombo.grid(row=2, column=2)

        Label(self.root, text='Издание', font=self.funny_font).grid(row=3, column=0)
        Label(self.root, text=str(old_values[2]), font=self.funny_font).grid(row=3, column=1)
        read_edits = DBAccessor.select_info(fr0m='Edition d JOIN Readings ON d.ID = Readings.ID_Edition',
                                            select='SELECT d.ID, d.Name, d.Cost')
        self.REditCombo = ttk.Combobox(self.root, values=read_edits)
        self.REditCombo.bind('<<ComboboxSelected>>', lambda e: self.combo_change('Edit'))
        self.REditCombo.grid(row=3, column=2)

        Label(self.root, text='Срок', font=self.funny_font).grid(row=4, column=0)
        Label(self.root, text=str(old_values[3]), font=self.funny_font).grid(row=4, column=1)
        self.RTermVar = StringVar(self.root, str(old_values[3]))
        Entry(self.root, text=self.RTermVar, font=self.funny_font).grid(row=4, column=2)
        self.RTermVar.trace('w', self.scan_enabling)

        self.root.mainloop()

    def combo_change(self, type):
        if type == 'Edit':
            s = self.REditCombo.get()
            s = s.split(' ')[0]
            self.REditCombo.set(s)
        if type == 'Sub':
            s = self.RSubCombo.get()
            s = s.split(' ')[0]
            self.RSubCombo.set(s)
        self.scan_enabling()

    def scan_enabling(self, trash1=None, trash2=None, trash3=None):
        is_ok = True
        if self.VarID.get() != '':
            res = DBAccessor.intTryParse(self.VarID.get())
            if res[1]:
                row = DBAccessor.select_info(fr0m='Readings',
                                             where=f'WHERE ID Like {self.VarID.get()} AND ID NOT LIKE {str(self.old_values[0])}')
                if len(row) != 0:
                    is_ok = False
            else:
                is_ok = False
        else:
            is_ok = False

        if self.RSubCombo.get() == '':
            is_ok = False
        if self.REditCombo.get() == '':
            is_ok = False
        if self.RTermVar.get() != '':
            if not DBAccessor.intTryParse(self.RTermVar.get())[1]:
                is_ok = False
        else:
            is_ok = False
        self.set_execute_button_state(is_ok)

    def go(self):
        DBAccessor.update_reading(
            self.old_values[0], (self.VarID.get(), self.RSubCombo.get(), self.REditCombo.get(), self.RTermVar.get())
        )
        self.mainF.info_fill(Table.Readings)


class EditionUpdateForm(AbsUpdateForm):
    def __init__(self,old_values, main):
        super().__init__(old_values, main)
        Label(self.root, text='Название', font=self.funny_font).grid(row=2, column=0)
        Label(self.root, text=str(old_values[1]), font=self.funny_font).grid(row=2, column=1)
        self.ENameVar = StringVar(self.root, str(old_values[1]))
        Entry(self.root, textvariable=self.ENameVar, font=self.funny_font).grid(row=2, column=2)
        self.ENameVar.trace('w', self.scan_enabling)

        Label(self.root, text='Цена', font=self.funny_font).grid(row=3, column=0)
        Label(self.root, text=str(old_values[2]), font=self.funny_font).grid(row=3, column=1)
        self.ECostVar = StringVar(self.root, str(old_values[2]))
        Entry(self.root, textvariable=self.ECostVar, font=self.funny_font).grid(row=3, column=2)
        self.ECostVar.trace('w', self.scan_enabling)

        Label(self.root, text='ФОТО', font=self.funny_font).grid(row=4, column=0)

        self.old_image_name = old_values[3]
        if (self.old_image_name is None) or (self.old_image_name == 'None'):
            self.old_image_name = 'none.png'

        old_photo = Canvas(self.root, bg='grey', width=100, height=100)
        old_photo.grid(row=4, column=1)
        img = Image.open(DBAccessor.base_path + r"photos/editions/" + self.old_image_name)
        img.thumbnail((100, 100), Image.ANTIALIAS)
        imgEdt = itk.PhotoImage(img, master=self.root)
        old_photo.image = imgEdt
        old_photo.create_image(0, 0, anchor=NW, image=imgEdt)

        self.new_image_path = self.old_image_name
        self.new_photo = Canvas(self.root, bg='grey', width=100, height=100)
        self.new_photo.grid(row=4, column=2)
        imgNewEdit = itk.PhotoImage(img, master=self.root)
        self.new_photo.image = imgNewEdit
        self.new_photo.create_image(0, 0, anchor=NW, image=imgNewEdit)

        Button(self.root, text='Выбрать', command=self.change_photo).grid(row=5, column=2)

        self.root.mainloop()

    def scan_enabling(self, trash1=None, trash2=None, trash3=None):
        is_ok = True
        if self.VarID.get() != '':
            res = DBAccessor.intTryParse(self.VarID.get())
            if res[1]:
                row = DBAccessor.select_info(fr0m='Edition',
                                             where=f'WHERE ID Like {self.VarID.get()} AND ID NOT LIKE {str(self.old_values[0])}')
                if len(row) != 0:
                    is_ok = False
            else:
                is_ok = False
        else:
            is_ok = False

        if self.ENameVar.get() == '':
            is_ok = False

        if not DBAccessor.intTryParse(self.ECostVar.get()):
            is_ok = False
        self.set_execute_button_state(is_ok)

    def change_photo(self):
        filetypes = (("Изображение", "*.jpg *.jpeg *.png *.jfif"),
                     ('Любой', '*'))
        img_path = filedialog.askopenfilename(title='Открыть картинку', initialdir="/", filetypes=filetypes)
        if img_path:
            self.new_image_path = img_path
            img = Image.open(self.new_image_path)
            img.thumbnail((100, 100), Image.ANTIALIAS)
            imgNew = itk.PhotoImage(img, master=self.root)
            self.new_photo.delete('all')
            self.new_photo.image = imgNew
            self.new_photo.create_image(0, 0, anchor=NW, image=imgNew)

        self.scan_enabling()

    def define_image(self):
        new_image_name = self.old_image_name
        if self.new_image_path != self.old_image_name:
            new_image_name = self.new_image_path.split('/')[-1]
            photo_path = r'photos/editions/'
            shutil.copy(self.new_image_path, DBAccessor.base_path + photo_path + new_image_name)
        elif (new_image_name is None) or (new_image_name == 'None'):
            new_image_name = 'none.png'
        return new_image_name

    def go(self):
        new_image_name = self.define_image()
        DBAccessor.update_edition(self.old_values[0],
                                  (self.VarID.get(), self.ENameVar.get(), self.ECostVar.get(), new_image_name))
        self.mainF.info_fill(Table.Editions)


class SubscriberUpdateForm(AbsUpdateForm):
    def __init__(self, old_values, main):
        super().__init__(old_values, main)
        Label(self.root, text='Имя').grid(row=2, column=0)
        Label(self.root, text=str(old_values[1])).grid(row=2, column=1)
        self.SNameVariable = StringVar(self.root, str(old_values[1]))
        Entry(self.root, textvariable=self.SNameVariable).grid(row=2, column=2)
        self.SNameVariable.trace('w', self.scan_enabling)

        Label(self.root, text='Фамилия').grid(row=3, column=0)
        Label(self.root, text=str(old_values[2])).grid(row=3, column=1)
        self.SSureNameVariable = StringVar(self.root, str(old_values[2]))
        Entry(self.root, textvariable=self.SSureNameVariable).grid(row=3, column=2)
        self.SSureNameVariable.trace('w', self.scan_enabling)

        Label(self.root, text='Пол').grid(row=4, column=0)
        Label(self.root, text=str(old_values[3])).grid(row=4, column=1)
        is_male = 0
        if old_values[3] == 'М':
            is_male = 1
        self.SGenderVariable = BooleanVar(self.root, is_male)
        Checkbutton(self.root, variable=self.SGenderVariable, onvalue=1, offvalue=0, text='Мужик? ').grid(row=4,
                                                                                                          column=2)
        self.SGenderVariable.trace('w', self.scan_enabling)

        Label(self.root, text='ФОТО', font=self.funny_font).grid(row=5, column=0)
        self.old_image_name = old_values[4]
        if (self.old_image_name is None) or (self.old_image_name == 'None'):
            self.old_image_name = 'none.png'

        old_photo = Canvas(self.root, bg='grey', width=100, height=100)
        old_photo.grid(row=5, column=1)
        img = Image.open(DBAccessor.base_path + r"photos/subscribers/" + self.old_image_name)
        img.thumbnail((100, 100), Image.ANTIALIAS)
        imgEdt = itk.PhotoImage(img, master=self.root)
        old_photo.image = imgEdt
        old_photo.create_image(0, 0, anchor=NW, image=imgEdt)

        self.new_image_path = self.old_image_name
        self.new_photo = Canvas(self.root, bg='grey', width=100, height=100)
        self.new_photo.grid(row=5, column=2)
        imgNewEdit = itk.PhotoImage(img, master=self.root)
        self.new_photo.image = imgNewEdit
        self.new_photo.create_image(0, 0, anchor=NW, image=imgNewEdit)
        Button(self.root, text='Выбрать', command=self.change_photo).grid(row=6, column=2)

        self.root.mainloop()

    def change_photo(self):
        filetypes = (("Изображение", "*.jpg *.jpeg *.png *.jfif"),
                     ('Любой', '*'))
        img_path = filedialog.askopenfilename(title='Открыть картинку', initialdir="/", filetypes=filetypes)
        if img_path:
            self.new_image_path = img_path
            img = Image.open(self.new_image_path)
            img.thumbnail((100, 100), Image.ANTIALIAS)
            imgNew = itk.PhotoImage(img, master=self.root)
            self.new_photo.delete('all')
            self.new_photo.image = imgNew
            self.new_photo.create_image(0, 0, anchor=NW, image=imgNew)

        self.scan_enabling()

    def scan_enabling(self, trash1=None, trash2=None, trash3=None):
        is_ok = True
        if self.VarID.get() != '':
            res = DBAccessor.intTryParse(self.VarID.get())
            if res[1]:
                row = DBAccessor.select_info(fr0m='Subscriber',
                                             where=f'WHERE ID Like {self.VarID.get()} AND ID NOT LIKE {str(self.old_values[0])}')
                if len(row) != 0:
                    is_ok = False
            else:
                is_ok = False
        else:
            is_ok = False

        if self.SNameVariable.get() == '':
            is_ok = False
        if self.SSureNameVariable.get() == '':
            is_ok = False

        self.set_execute_button_state(is_ok)

    def define_image(self):
        new_image_name = self.old_image_name
        if self.new_image_path != self.old_image_name:
            new_image_name = self.new_image_path.split('/')[-1]
            photo_path = r'photos/subscribers/'
            shutil.copy(self.new_image_path, DBAccessor.base_path + photo_path + new_image_name)
        elif (new_image_name is None) or (new_image_name == 'None'):
            new_image_name = 'none.png'
        return new_image_name

    def go(self):
        new_image_name = self.define_image()
        DBAccessor.update_subscriber(self.old_values[0],
                                     (self.VarID.get(), self.SNameVariable.get(), self.SSureNameVariable.get(),
                                      'М' if self.SGenderVariable.get() == 1 else 'Ж', new_image_name))
        self.mainF.info_fill(Table.Subscribers)
        super().go()



