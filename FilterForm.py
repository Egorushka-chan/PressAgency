from tkinter import *
from tkinter import font
from model.tkSliderWidget import Slider
import DBAccessor


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
