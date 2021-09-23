from tkinter import *
from tkinter import ttk, font, filedialog
from model.tkSliderWidget import Slider
import DBAccessor
from PIL import Image
from PIL import ImageTk as itk
import shutil


class FilterForm:
    def __init__(self, main):
        self.mainF = main
        self.root = Tk()
        self.root.title('Фильтрация')

        self.century_gothic = font.Font(family="Century Gothic", size=12)

        self.radioFrame = Frame(self.root)
        self.radioFrame.grid(column=0, row=0)
        self.radioVar = IntVar(self.root)
        self.radioVar.set(1)
        self.radioVar.trace("w", self.radio_change)
        Radiobutton(self.radioFrame, font=self.century_gothic, text='Издания', variable=self.radioVar, value=1).pack(
            side='left')
        Radiobutton(self.radioFrame, font=self.century_gothic, text='Подписчики', variable=self.radioVar, value=2).pack(
            side='left')
        Radiobutton(self.radioFrame, font=self.century_gothic, text='Выписки', variable=self.radioVar, value=3).pack(
            side='left')

        self.valuesColumnSub = ['ID', 'Имя', 'Фамилия']
        self.valuesColumnEdit = ['ID', 'Название', 'Стоимость']
        self.valuesColumnRead = ['ID', 'Издание', 'Подписчик', 'Срок']
        self.valuesType = ['IS', 'NULL', 'AND', 'OR', 'IN', 'NOT', 'LIKE', '=']

        self.main_frame = Frame(self.root)

        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

        self.root.mainloop()

    def radio_change(self, event=None, trace=None, cmd=None):
        self.main_frame.destroy()
        self.main_frame = Frame(self.root)
        if self.radioVar.get() == 1:
            row = DBAccessor.select_info(fr0m="Edition", select="SELECT Max(ID)")
            Label(self.main_frame, text='ID', font=self.century_gothic).grid(row=0, column=0)
            self.first_slider = Slider(self.main_frame, width=300, min_val=1, max_val=row[0][0],
                                       init_lis=[1, row[0][0]], show_value=True, moving_method=self.first_filter)
            self.first_slider.grid(row=0, column=1)

            izd_name_frame = Frame(self.main_frame)
            izd_name_frame.grid(row=1, columnspan=2)

            Label(izd_name_frame, font=self.century_gothic, text='Имя ').grid(row=0, column=0)
            self.izd_name = StringVar(self.main_frame)
            Entry(izd_name_frame, font=self.century_gothic, textvariable=self.izd_name).grid(row=0, column=1)
            self.izd_name.trace("w", self.first_filter)

            self.is_extrended_fam = BooleanVar(self.main_frame)
            self.is_extrended_fam.set(1)
            Checkbutton(izd_name_frame, padx=3, font=self.century_gothic, text='Включение',
                        variable=self.is_extrended_fam, onvalue=1, offvalue=0).grid(row=0, column=2)
            self.is_extrended_fam.trace("w", self.first_filter)

            row = DBAccessor.select_info(fr0m="Edition", select="SELECT Max(Cost)")
            Label(self.main_frame, font=self.century_gothic, text='Цена').grid(row=2, column=0)
            self.second_slider = Slider(self.main_frame, width=300, min_val=0, max_val=row[0][0],
                                        init_lis=[0, row[0][0]], show_value=True, moving_method=self.first_filter)
            self.second_slider.grid(row=2, column=1)

        elif self.radioVar.get() == 2:

            row = DBAccessor.select_info(fr0m="Subscriber", select="SELECT Max(ID)")
            Label(self.main_frame, text='ID', font=self.century_gothic).grid(row=0, column=0)
            self.first_slider = Slider(self.main_frame, width=300, min_val=1, max_val=row[0][0],
                                       init_lis=[1, row[0][0]], show_value=True, moving_method=self.first_filter)
            self.first_slider.grid(row=0, column=1)

            izd_name_frame = Frame(self.main_frame)
            izd_name_frame.grid(row=1, columnspan=2)

            Label(izd_name_frame, font=self.century_gothic, text='Имя ').grid(row=0, column=0)
            self.izd_name = StringVar(self.main_frame)
            Entry(izd_name_frame, font=self.century_gothic, textvariable=self.izd_name).grid(row=0, column=1)
            self.izd_name.trace("w", self.first_filter)

            self.is_extrended_fam = BooleanVar(self.main_frame)
            self.is_extrended_fam.set(1)
            Checkbutton(izd_name_frame, padx=3, font=self.century_gothic, text='Включение',
                        variable=self.is_extrended_fam, onvalue=1, offvalue=0).grid(row=0, column=2)
            self.is_extrended_fam.trace("w", self.first_filter)

            Label(self.main_frame, font=self.century_gothic, text='Пол:').grid(row=2, column=0)
            self.gender = BooleanVar(self.main_frame, 1)
            Checkbutton(self.main_frame, variable=self.gender, onvalue=1, offvalue=0, text='Мужик',
                        font=self.century_gothic).grid(row=2, column=1)
            self.gender.trace('w', self.first_filter)

        elif self.radioVar.get() == 3:
            row = DBAccessor.select_info(fr0m="Readings", select="SELECT Max(ID)")
            Label(self.main_frame, text='ID', font=self.century_gothic).grid(row=0, column=0)
            self.first_slider = Slider(self.main_frame, width=300, min_val=1, max_val=row[0][0],
                                       init_lis=[1, row[0][0]], show_value=True, moving_method=self.first_filter)
            self.first_slider.grid(row=0, column=1)

            row = DBAccessor.select_info(fr0m="Readings", select="SELECT Max(Sub_Term)")
            Label(self.main_frame, font=self.century_gothic, text='Срок').grid(row=1, column=0)
            self.second_slider = Slider(self.main_frame, width=300, min_val=0, max_val=row[0][0],
                                        init_lis=[0, row[0][0]], show_value=True, moving_method=self.first_filter)
            self.second_slider.grid(row=1, column=1)

            izd_name_frame = Frame(self.main_frame)
            izd_name_frame.grid(row=2, columnspan=2)

            Label(izd_name_frame, font=self.century_gothic, text='Изд. ').grid(row=0, column=0)
            self.izd_name = StringVar(self.main_frame)
            Entry(izd_name_frame, font=self.century_gothic, textvariable=self.izd_name).grid(row=0, column=1)
            self.izd_name.trace("w", self.first_filter)

            sub_name_frame = Frame(self.main_frame)
            sub_name_frame.grid(row=3, columnspan=2)

            Label(sub_name_frame, font=self.century_gothic, text='Подп. ', pady=5).grid(row=0, column=0)
            self.sub_name = StringVar(self.main_frame)
            Entry(sub_name_frame, font=self.century_gothic, textvariable=self.sub_name).grid(row=0, column=1)
            self.sub_name.trace("w", self.first_filter)

        self.main_frame.grid(row=1, column=0)

    def first_filter(self, event=None, trace=None, cmd=None):
        where = "WHERE 1 = 1"
        fr0m = "Edition"
        if self.radioVar.get() == 1:
            fr0m = "Edition"
            values_id = self.first_slider.getValues()
            values_cost = self.second_slider.getValues()
            where = f"WHERE (ID BETWEEN {values_id[0]} AND {values_id[1]}) AND (Cost BETWEEN {values_cost[0]} AND {values_cost[1]}) "
            if len(self.izd_name.get()) > 0:
                name = self.izd_name.get()
                if self.is_extrended_fam.get() == 1:
                    name = '%' + name + '%'
                where = where + "AND Name LIKE '" + name + "'"
        elif self.radioVar.get() == 2:
            fr0m = "Subscriber"
            values_id = self.first_slider.getValues()

            gender_value = 'М' if self.gender.get() == 1 else 'Ж'

            where = f'WHERE (ID BETWEEN {values_id[0]} AND {values_id[1]}) AND (Gender Like "{gender_value}") '
            if len(self.izd_name.get()) > 0:
                name = self.izd_name.get()
                if self.is_extrended_fam.get() == 1:
                    name = '%' + name + '%'
                where = where + "AND Name LIKE '" + name + "'"
        elif self.radioVar.get() == 3:
            fr0m = 'vReadings'
            values_id = self.first_slider.getValues()
            values_term = self.second_slider.getValues()
            where = f"WHERE (ID BETWEEN {values_id[0]} AND {values_id[1]}) " \
                    f"AND (Sub_Term Between {values_term[0]} AND {values_term[1]}) "
            if len(self.sub_name.get()) > 0:
                name = self.sub_name.get()
                name = '%' + name + '%'
                where = where + "AND Subscriber LIKE '" + name + "'"
            if len(self.izd_name.get()) > 0:
                name = self.izd_name.get()
                name = '%' + name + '%'
                where = where + " AND Name LIKE '" + name + "'"

        self.mainF.begin_filter(fr0m, where, self.radioVar.get())

    def on_closing(self):
        self.mainF.info_fill()
        self.root.destroy()


class ChangeForm:
    def __init__(self, table, old_values, main):
        self.mainF = main
        self.old_values = old_values
        self.table = table
        self.root = Tk()
        self.funny_font = font.Font(font='Arial', size=12)
        self.root.title('Изменить ' + table)

        Label(self.root, text='Поле', font=self.funny_font).grid(row=0, column=0)
        Label(self.root, text='Текущее', font=self.funny_font).grid(row=0, column=1)
        Label(self.root, text='Новое', font=self.funny_font).grid(row=0, column=2)
        Label(self.root, text='ID', font=self.funny_font).grid(row=1, column=0)

        self.VarID = StringVar(self.root, str(old_values[0]))
        Label(self.root, text=str(old_values[0]), font=self.funny_font).grid(row=1, column=1)
        Entry(self.root, text=self.VarID, font=self.funny_font).grid(row=1, column=2)
        self.VarID.trace('w', self.scan_enabling)
        if table == 'Readings':
            Label(self.root, text='Подписчик', font=self.funny_font).grid(row=2, column=0)
            Label(self.root, text=str(self.old_values[1]), font=self.funny_font).grid(row=2, column=1)
            read_subs = DBAccessor.select_info(select='SELECT d.ID, d.Name, d.Surname',
                                               fr0m='Subscriber d JOIN Readings ON d.ID = Readings.ID_Subscriber')
            self.RSubCombo = ttk.Combobox(self.root, values=read_subs)
            self.RSubCombo.bind('<<ComboboxSelected>>', lambda e: self.combo_change('Sub'))
            self.RSubCombo.grid(row=2, column=2)

            Label(self.root, text='Издание', font=self.funny_font).grid(row=3, column=0)
            Label(self.root, text=str(old_values[2]), font=self.funny_font).grid(row=3, column=1)
            read_edits = DBAccessor.select_info(select='SELECT d.ID, d.Name, d.Cost',
                                                fr0m='Edition d JOIN Readings ON d.ID = Readings.ID_Edition')
            self.REditCombo = ttk.Combobox(self.root, values=read_edits)
            self.REditCombo.bind('<<ComboboxSelected>>', lambda e: self.combo_change('Edit'))
            self.REditCombo.grid(row=3,column=2)

            Label(self.root, text = 'Срок', font = self.funny_font).grid(row=4, column=0)
            Label(self.root, text = str(old_values[3]), font = self.funny_font).grid(row =4, column=1)
            self.RTermVar = StringVar(self.root, str(old_values[3]))
            Entry(self.root, text=self.RTermVar, font=self.funny_font).grid(row=4,column=2)
            self.RTermVar.trace('w', self.scan_enabling)
        elif table == 'Editions':
            Label(self.root, text='Название', font=self.funny_font).grid(row=2, column=0)
            Label(self.root, text=str(old_values[1]), font=self.funny_font).grid(row=2,column=1)
            self.ENameVar = StringVar(self.root, str(old_values[1]))
            Entry(self.root, textvariable=self.ENameVar, font=self.funny_font).grid(row=2, column=2)
            self.ENameVar.trace('w', self.scan_enabling)

            Label(self.root, text='Цена', font=self.funny_font).grid(row=3, column=0)
            Label(self.root, text=str(old_values[2]), font=self.funny_font).grid(row=3,column=1)
            self.ECostVar = StringVar(self.root, str(old_values[2]))
            Entry(self.root, textvariable=self.ECostVar, font=self.funny_font).grid(row=3, column=2)
            self.ECostVar.trace('w', self.scan_enabling)

            Label(self.root, text='ФОТО', font=self.funny_font).grid(row=4,column=0)

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
            self.new_photo = Canvas(self.root, bg='grey', width=100, height = 100)
            self.new_photo.grid(row=4,column=2)
            imgNewEdit = itk.PhotoImage(img, master=self.root)
            self.new_photo.image = imgNewEdit
            self.new_photo.create_image(0,0, anchor=NW, image= imgNewEdit)

            Button(self.root, text='Выбрать', command =self.change_photo).grid(row=5, column=2)
        elif table == 'Subscribers':
            Label(self.root, text='Имя').grid(row=2, column=0)
            Label(self.root, text=str(old_values[1])).grid(row=2, column=1)
            self.SNameVariable = StringVar(self.root, str(old_values[1]))
            Entry(self.root, textvariable=self.SNameVariable).grid(row=2, column=2)
            self.SNameVariable.trace('w', self.scan_enabling)

            Label(self.root, text='Фамилия').grid(row=3, column=0)
            Label(self.root, text=str(old_values[2])).grid(row=3,column=1)
            self.SSureNameVariable = StringVar(self.root, str(old_values[2]))
            Entry(self.root, textvariable=self.SSureNameVariable).grid(row=3, column=2)
            self.SSureNameVariable.trace('w', self.scan_enabling)

            Label(self.root, text='Пол').grid(row=4, column=0)
            Label(self.root, text=str(old_values[3])).grid(row=4,column=1)
            is_male = 0
            if old_values[3] == 'М':
                is_male = 1
            self.SGenderVariable = BooleanVar(self.root, is_male)
            Checkbutton(self.root, variable=self.SGenderVariable, onvalue=1, offvalue=0,text='Мужик? ').grid(row=4, column=2)
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

        self.enter_button = Button(self.root, text='Изменить', state=DISABLED, font=self.funny_font, command=self.go)
        self.enter_button.grid(row=10, columnspan=3)

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
        if self.table == 'Readings':
            if self.VarID.get() != '':
                res = DBAccessor.intTryParse(self.VarID.get())
                if res[1]:
                    row = DBAccessor.select_info(fr0m='Readings', where=f'WHERE ID Like {self.VarID.get()} AND ID NOT LIKE {str(self.old_values[0])}')
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
        elif self.table == 'Edition':
            if self.VarID.get() != '':
                res = DBAccessor.intTryParse(self.VarID.get())
                if res[1]:
                    row = DBAccessor.select_info(fr0m='Edition', where=f'WHERE ID Like {self.VarID.get()} AND ID NOT LIKE {str(self.old_values[0])}')
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
        elif self.table == 'Subscribers':
            if self.VarID.get() != '':
                res = DBAccessor.intTryParse(self.VarID.get())
                if res[1]:
                    row = DBAccessor.select_info(fr0m='Subscriber', where=f'WHERE ID Like {self.VarID.get()} AND ID NOT LIKE {str(self.old_values[0])}')
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
        if is_ok:
            self.enter_button['state'] = 'normal'
        else:
            self.enter_button['state'] = 'disabled'


    def go(self):
        if self.table == 'Readings':
            DBAccessor.update_reading(
                self.old_values[0], (self.VarID.get(), self.RSubCombo.get(), self.REditCombo.get(), self.RTermVar.get())
            )
            self.mainF.info_fill('Readings')
        elif self.table == 'Editions':
            new_image_name = self.define_image()
            DBAccessor.update_edition(self.old_values[0], (self.VarID.get(), self.ENameVar.get(), self.ECostVar.get(), new_image_name))
            self.mainF.info_fill('Editions')
        elif self.table == 'Subscribers':
            new_image_name = self.define_image()
            DBAccessor.update_subscriber(self.old_values[0],
                                      (self.VarID.get(), self.SNameVariable.get(), self.SSureNameVariable.get(), self.SGenderVariable.get(), new_image_name))
            self.mainF.info_fill('Sub')
        self.root.destroy()

    def define_image(self):
        new_image_name = self.old_image_name
        if self.new_image_path != self.old_image_name:
            new_image_name = self.new_image_path.split('/')[-1]
            photo_path = r'photos/editions/'
            if self.table == 'Subscribers':
                photo_path = r'photos/subscribers/'
            shutil.copy(self.new_image_path, DBAccessor.base_path + photo_path + new_image_name)
        elif (new_image_name is None) or (new_image_name == 'None'):
            new_image_name = 'none.png'
        return new_image_name

