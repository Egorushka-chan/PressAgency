from tkinter import *
from tkinter import ttk, font, filedialog
from model.tkSliderWidget import Slider
import DBAccessor
from PIL import Image
from PIL import ImageTk as itk
import shutil
from model.AbsInsertForm import AbsInsertForm
from model.TableEnum import Table


class ReadingInsertForm(AbsInsertForm):
    def __init__(self, main):
        super().__init__(main)
        self.root.title('Добавить Подписку!')

        Label(self.root, text='ID', font=self.funny_font).grid(row=0, column=0)
        max_id = DBAccessor.select_info(fr0m="Readings", select="SELECT (Max(ID) + 1) as `da`")[0][0]
        self.RIdVariable = StringVar(self.root, str(max_id))
        Entry(self.root, textvariable=self.RIdVariable, font=self.funny_font).grid(row=0, column=1)
        self.RIdVariable.trace('w', self.scan_enability)

        Label(self.root, text='Издание').grid(row=1, column=0)
        values_edit = DBAccessor.select_info(fr0m='Edition', select="SELECT ID, Name, Cost")
        self.REditCombo = ttk.Combobox(self.root, values=values_edit)
        self.REditCombo.bind("<<ComboboxSelected>>", lambda e: self.combo_change('Edit'))
        self.REditCombo.grid(row=1, column=1)

        Label(self.root, text='Подписчик ').grid(row=2, column=0)
        values_sub = DBAccessor.select_info(fr0m='Subscriber', select="SELECT ID, (Surname || ' ' || Name) As Full")
        self.RSubCombo = ttk.Combobox(self.root, values=values_sub)
        self.RSubCombo.bind("<<ComboboxSelected>>", lambda e: self.combo_change('Sub'))
        self.RSubCombo.grid(row=2, column=1)

        Label(self.root, text='Срок').grid(row=3, column=0)
        self.RTermVariable = StringVar(self.root, 1)
        Entry(self.root, textvariable=self.RTermVariable).grid(row=3, column=1)
        self.RTermVariable.trace('w', self.scan_enability)
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
        self.scan_enability()

    def scan_enability(self, trash1=None, trash2=None, trash3=None):
        is_ok = True
        if self.RIdVariable.get() != '':
            res = DBAccessor.intTryParse(self.RIdVariable.get())
            if res[1]:
                row = DBAccessor.select_info(fr0m='Readings', where=f'WHERE ID Like {self.RIdVariable.get()}')
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
        if self.RTermVariable.get() != '':
            if not DBAccessor.intTryParse(self.RTermVariable.get())[1]:
                is_ok = False
        else:
            is_ok = False
        if is_ok:
            self.enter_button['state'] = 'normal'
        else:
            self.enter_button['state'] = 'disabled'

    def go(self):
        DBAccessor.insert_reading(
            (self.RIdVariable.get(), self.RSubCombo.get(), self.REditCombo.get(), self.RTermVariable.get()))
        self.mainF.info_fill(Table.Readings)


class EditionInsertForm(AbsInsertForm):

    def __init__(self, main):
        super().__init__(main)

        self.root.title('Добавить новое Издание')
        Label(self.root, text='ID', font=self.funny_font).grid(row=0, column=0)
        max_id = DBAccessor.select_info(fr0m="Edition", select="SELECT (Max(ID) + 1) as `da`")[0][0]
        self.EIdVariable = StringVar(self.root, str(max_id))
        Entry(self.root, textvariable=self.EIdVariable, font=self.funny_font).grid(row=0, column=1)
        self.EIdVariable.trace('w', self.scan_enability)

        Label(self.root, text='Название').grid(row=1, column=0)
        self.ENameVariable = StringVar(self.root)
        Entry(self.root, textvariable=self.ENameVariable).grid(row=1, column=1)
        self.ENameVariable.trace('w', self.scan_enability)

        Label(self.root, text='Цена').grid(row=1, column=0)
        self.ECostVariable = StringVar(self.root, 100)
        Entry(self.root, textvariable=self.ENameVariable).grid(row=1, column=1)
        self.ECostVariable.trace('w', self.scan_enability)
        self.root.mainloop()

    def scan_enability(self, trash1=None, trash2=None, trash3=None):
        is_ok = True
        if self.EIdVariable.get() != '':
            row = DBAccessor.select_info(fr0m='Edition', where=f'WHERE ID Like {self.EIdVariable.get()}')
            if len(row) != 0:
                is_ok = False
            res = DBAccessor.intTryParse(self.EIdVariable.get())

            if not res:
                is_ok = False
        else:
            is_ok = False

        if self.ENameVariable.get() == '':
            is_ok = False

        if self.ENameVariable.get() == '':
            is_ok = False

        if not DBAccessor.intTryParse(self.ENameVariable.get()):
            is_ok = False
        if is_ok:
            self.enter_button['state'] = 'normal'
        else:
            self.enter_button['state'] = 'disabled'

    def go(self):
        DBAccessor.insert_edition((self.EIdVariable.get(), self.ENameVariable.get(), self.ECostVariable.get()))
        self.mainF.info_fill(Table.Editions)


class SubscriberInsertForm(AbsInsertForm):

    def __init__(self, main):
        super().__init__(main)

        self.root.title('Добавить нового попищека!')
        Label(self.root, text='ID', font=self.funny_font).grid(row=0, column=0)
        max_id = DBAccessor.select_info(fr0m="Subscriber", select="SELECT (Max(ID) + 1) as `da`")[0][0]
        self.SIdVariable = StringVar(self.root, str(max_id))
        Entry(self.root, textvariable=self.SIdVariable, font=self.funny_font).grid(row=0, column=1)
        self.SIdVariable.trace('w', self.scan_enability)

        Label(self.root, text='Имя').grid(row=1, column=0)
        self.SNameVariable = StringVar(self.root)
        Entry(self.root, textvariable=self.SNameVariable).grid(row=1, column=1)
        self.SNameVariable.trace('w', self.scan_enability)

        Label(self.root, text='Фамилия').grid(row=2, column=0)
        self.SSureNameVariable = StringVar(self.root)
        Entry(self.root, textvariable=self.SSureNameVariable).grid(row=2, column=1)
        self.SSureNameVariable.trace('w', self.scan_enability)

        Label(self.root, text='Мужик').grid(row=3, column=0)
        self.SGenderVariable = BooleanVar(self.root, 1)
        Checkbutton(self.root, variable=self.SGenderVariable, onvalue=1, offvalue=0).grid(row=3, column=1)
        self.SGenderVariable.trace('w', self.scan_enability)

        self.root.mainloop()

    def scan_enability(self, trash1=None, trash2=None, trash3=None):
        is_ok = True
        if self.SIdVariable.get() != '':
            row = DBAccessor.select_info(fr0m='Subscriber', where=f'WHERE ID Like {self.SIdVariable.get()}')
            if len(row) != 0:
                is_ok = False
            res = DBAccessor.intTryParse(self.SIdVariable.get())
            if not res:
                is_ok = False
        else:
            is_ok = False

        if self.SNameVariable.get() == '':
            is_ok = False
        if self.SSureNameVariable.get() == '':
            is_ok = False
        if is_ok:
            self.enter_button['state'] = 'normal'
        else:
            self.enter_button['state'] = 'disabled'

    def go(self):
        DBAccessor.insert_subscriber((
            self.SIdVariable.get(), self.SNameVariable.get(), self.SSureNameVariable.get(),
            'М' if self.SGenderVariable.get() == 1 else 'Ж'))
        self.mainF.info_fill(Table.Subscribers)
