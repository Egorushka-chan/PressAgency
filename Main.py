from tkinter import *
from tkinter import ttk, font, messagebox

from PIL import Image
from PIL import ImageTk as itk

import FilterForm
import InsertForms
import DBAccessor
import UpdateForms
import model.AbsUpdateForm
from model.user import UserRank, User
from model.TableEnum import Table


class LoginForm:
    def __init__(self):
        self.main = mainF
        self.root = Tk()
        self.root.title('Логин')
        Label(self.root, text='Логин').grid(row=0, column=0)
        Label(self.root, text='Пароль').grid(row=1, column=0)
        self.loginEntry = Entry(self.root)
        self.loginEntry.grid(row=0, column=1, pady=10)
        self.passEntry = Entry(self.root)
        self.passEntry.grid(row=1, column=1)

        img = Image.open(DBAccessor.base_path + r"photos/program/pressIcon.png")
        imgItk = itk.PhotoImage(img, master=self.root)
        self.root.iconphoto(True, imgItk)
        # rows = DBAccessor.select_info(fr0m='Types')
        # type_values = []
        # for row in rows:
        #     type_values.insert(len(type_values), row[1])
        # self.typeVar = StringVar(self.root)
        # ttk.Combobox(self.root, textvariable=self.typeVar, values=type_values).grid(column=2, rowspan=2, row=0)
        Button(self.root, text='Подтвердить', command=self.validate).grid(row=3, columnspan=3)
        self.root.mainloop()

    def validate(self):
        rows_V = DBAccessor.select_info(fr0m='Users JOIN Types ON Users.Type=Types.ID',
                                        where=f'WHERE Users.Login = "{self.loginEntry.get()}" AND Users.Password = "{self.passEntry.get()}"')

        if len(rows_V) == 1:
            role = UserRank.employee
            if int(rows_V[0][2]) == 2:
                role = UserRank.admin
            elif int(rows_V[0][2]) == 3:
                role = UserRank.intern

            currentUser = User(rows_V[0][0], role)

            self.main(currentUser, self)
        elif len(rows_V) > 1:
            messagebox.showerror("Больше одного пользователя", f'Кол-во={len(rows_V)}')
        else:
            messagebox.showerror('Незаход', 'Пользователь не найден')
        return False


class mainF:
    def __init__(self, currentUser, login=None):
        self.currentUser = currentUser
        self.main_window = Tk()
        self.main_window.title('Подписное агенство "Пресса"')

        self.main_menu = Menu(self.main_window)
        self.main_window.config(menu=self.main_menu)

        self.file_menu = Menu(self.main_menu, tearoff=0)
        if self.currentUser.rank in (UserRank.employee, UserRank.admin):
            self.file_menu.add_command(label='Новая подписка', accelerator="Ctrl+N",
                                       command=lambda: self.new_item(Table.Readings))
            self.main_menu.bind_all("<Control-n>", lambda event: self.new_item(Table.Readings))
            self.file_menu.add_command(label='Изменить подписку', command=lambda: self.change_item(Table.Readings))
            self.file_menu.add_command(label='Удалить подписку', command=lambda: self.delete_item(Table.Readings))
            self.file_menu.add_separator()
        self.file_menu.add_command(label='Фильтрация', accelerator="Ctrl+F", command=self.open_filter)
        self.main_menu.bind_all("<Control-f>", self.open_filter)
        self.file_menu.add_separator()
        self.report_file_menu = Menu(self.file_menu, tearoff=0)
        self.report_file_menu.add_command(label='Подписчики по изданиям')
        self.report_file_menu.add_command(label='Реестр подписчиков')
        self.report_file_menu.add_command(label='Рейтинг изданий')
        self.file_menu.add_cascade(label='Отчеты', menu=self.report_file_menu)
        self.file_menu.add_separator()
        self.file_menu.add_command(label='Выход', accelerator="Ctrl+Q", command=quit)
        self.main_window.bind_all("<Control-q>", quit)

        if self.currentUser.rank in (UserRank.employee, UserRank.admin):
            self.sub_menu = Menu(self.main_menu, tearoff=0)
            self.sub_menu.add_command(label='Новый подписчик', command=lambda: self.new_item(Table.Subscribers))
            if self.currentUser.rank is UserRank.admin:
                self.sub_menu.add_command(label='Изменить подписчика',
                                          command=lambda: self.change_item(Table.Subscribers))
                self.sub_menu.add_command(label='Удалить подписчика',
                                          command=lambda: self.delete_item(Table.Subscribers))

        if self.currentUser.rank in (UserRank.employee, UserRank.admin):
            self.edition_menu = Menu(self.main_menu, tearoff=0)
            self.edition_menu.add_command(label='Новое издание', command=lambda: self.new_item(Table.Editions))
            if self.currentUser.rank is UserRank.admin:
                self.edition_menu.add_command(label='Изменить издание',
                                              command=lambda: self.change_item(Table.Editions))
                self.edition_menu.add_command(label='Удалить издание', command=lambda: self.delete_item(Table.Editions))

        self.help_menu = Menu(self.main_menu, tearoff=0)
        self.help_menu.add_command(label='О программе', accelerator="Ctrl+H")

        self.main_menu.add_cascade(label='Файл', menu=self.file_menu)
        if self.currentUser.rank in (UserRank.employee, UserRank.admin):
            self.main_menu.add_cascade(label='Подписчики', menu=self.sub_menu)
            self.main_menu.add_cascade(label='Издания', menu=self.edition_menu)
        self.main_menu.add_cascade(label='Справка', menu=self.help_menu)

        self.century_gothic = font.Font(family="Century Gothic", size=11)
        Label(self.main_window, text='Подписки', font=self.century_gothic).grid(column=1, row=1)

        self.tableReadingsFrame = Frame(self.main_window)
        tab_read_columns = ('1', '2', '3', '4')
        self.tableReadings = ttk.Treeview(self.tableReadingsFrame, columns=tab_read_columns, show='headings', height=25)
        for col in tab_read_columns:
            self.tableReadings.heading(col, text=col, command=lambda _col=col: \
                self.treeview_sort_column(self.tableReadings, _col, False))

        self.tableReadings.pack(side='right')
        self.verscrlbar = ttk.Scrollbar(self.tableReadingsFrame, orient="vertical", command=self.tableReadings.yview)
        self.verscrlbar.pack(side='left', fill='y')
        self.tableReadings.configure(yscrollcommand=self.verscrlbar.set)

        self.tableReadings.column("1", width=90, anchor='c')
        self.tableReadings.column("2", width=90, anchor='c')
        self.tableReadings.column("3", width=90, anchor='c')
        self.tableReadings.column("4", width=90, anchor='c')

        self.tableReadings.heading("1", text='ID')
        self.tableReadings.heading("2", text='Издание')
        self.tableReadings.heading("3", text='Подписчик')
        self.tableReadings.heading("4", text='Срок')

        self.tableReadingsFrame.grid(rowspan=4, row=2, column=1, padx=10, pady=5)

        Label(self.main_window, text='Подписчики', font=self.century_gothic).grid(column=2, row=1)

        self.tableSubscribersFrame = Frame(self.main_window)
        tab_sub_columns = ("1", "2", "3")
        self.tableSubscribers = ttk.Treeview(self.tableSubscribersFrame, columns=tab_sub_columns, show='headings')
        for col in tab_sub_columns:
            self.tableSubscribers.heading(col, text=col, command=lambda _col=col: \
                self.treeview_sort_column(self.tableSubscribers, _col, False))
        self.tableSubscribers.bind("<<TreeviewSelect>>", lambda x: self.trev_select(place='Sub', event=x))

        self.tableSubscribers.pack(side='right')
        self.verscrlbar1 = ttk.Scrollbar(self.tableSubscribersFrame, orient="vertical",
                                         command=self.tableSubscribers.yview)
        self.verscrlbar1.pack(side='left', fill='y')
        self.tableSubscribers.configure(yscrollcommand=self.verscrlbar1.set)

        self.tableSubscribers.column("1", width=90, anchor='c')
        self.tableSubscribers.column("2", width=90, anchor='c')
        self.tableSubscribers.column("3", width=90, anchor='c')

        self.tableSubscribers.heading("1", text='ID')
        self.tableSubscribers.heading("2", text='Имя')
        self.tableSubscribers.heading("3", text='Фамилия')

        self.tableSubscribersFrame.grid(row=2, column=2, padx=10, pady=5)

        Label(self.main_window, text='Издания', font=self.century_gothic).grid(column=2, row=4)

        self.tableEditionsFrame = Frame(self.main_window)
        tab_edit_columns = ("1", "2", "3")
        self.tableEditions = ttk.Treeview(self.tableEditionsFrame, show='headings', columns=tab_edit_columns)
        for col in tab_edit_columns:
            self.tableEditions.heading(col, text=col, command=lambda _col=col: \
                self.treeview_sort_column(self.tableEditions, _col, False))
        self.tableEditions.bind("<<TreeviewSelect>>", lambda x: self.trev_select(place='Edit', event=x))

        self.tableEditions.pack(side='right')
        self.verscrlbar2 = ttk.Scrollbar(self.tableEditionsFrame, orient="vertical", command=self.tableEditions.yview)
        self.verscrlbar2.pack(side='left', fill='y')
        self.tableEditions.configure(yscrollcommand=self.verscrlbar2.set)

        self.tableEditions.column("1", width=90, anchor='c')
        self.tableEditions.column("2", width=90, anchor='c')
        self.tableEditions.column("3", width=90, anchor='c')

        self.tableEditions.heading("1", text='ID')
        self.tableEditions.heading("2", text='Название')
        self.tableEditions.heading("3", text='Стоимость')

        self.tableEditionsFrame.grid(row=5, column=2, padx=10, pady=5)

        self.cnvScrb = Canvas(self.main_window, bg='grey', width=225, height=225)
        self.cnvEdt = Canvas(self.main_window, bg='grey', width=225, height=225)

        self.cnvScrb.grid(column=3, row=2)
        self.cnvEdt.grid(column=3, row=5)

        # --Страницы--

        self.countDataReadings = Frame(self.main_window)
        Label(self.countDataReadings, text='Кол-во:').pack(side='left')
        self.cDRSelected = IntVar(self.main_menu, 50)
        self.cDR50 = Label(self.countDataReadings, text='50', fg='blue')
        self.cDR50.pack(side='left')
        self.cDR50.bind("<Button-1>", lambda e: (self.cDRSelected.set(50), self.info_fill(Table.Readings)))
        self.cDR200 = Label(self.countDataReadings, text='200', fg='blue')
        self.cDR200.pack(side='left')
        self.cDR200.bind("<Button-1>", lambda e: (self.cDRSelected.set(200), self.info_fill(Table.Readings)))
        self.cDR500 = Label(self.countDataReadings, text='500', fg='blue')
        self.cDR500.pack(side='left')
        self.cDR500.bind("<Button-1>", lambda e: (self.cDRSelected.set(500), self.info_fill(Table.Readings)))
        Label(self.countDataReadings, padx=10, text='Всего:').pack(side='left')
        row = DBAccessor.select_info(fr0m="Readings", select="SELECT COUNT(ID)")
        self.cDRTotal = Label(self.countDataReadings, fg='red', text=str(row[0][0]))
        self.cDRTotal.pack(side='left')

        Button(self.countDataReadings, text='<', width=3,
               command=lambda: self.change_paragraph('<', Table.Readings)).pack(
            side='left')
        self.cDRCurrent = IntVar(self.main_menu, 0)
        Label(self.countDataReadings, textvariable=self.cDRCurrent).pack(side='left')
        Button(self.countDataReadings, text='>', width=3,
               command=lambda: self.change_paragraph('>', Table.Readings)).pack(
            side='left')
        self.countDataReadings.grid(column=1, row=6)
        # --
        self.countDataSubscribers = Frame(self.main_window)
        Label(self.countDataSubscribers, text='Кол-во:').pack(side='left')
        self.cDSSelected = IntVar(self.main_menu, 20)
        self.cDS20 = Label(self.countDataSubscribers, text='20', fg='blue')
        self.cDS20.pack(side='left')
        self.cDS20.bind("<Button-1>", lambda e: (self.cDSSelected.set(20), self.info_fill(Table.Subscribers)))
        self.cDS100 = Label(self.countDataSubscribers, text='100', fg='blue')
        self.cDS100.pack(side='left')
        self.cDS100.bind("<Button-1>", lambda e: (self.cDSSelected.set(100), self.info_fill(Table.Subscribers)))
        self.cDS200 = Label(self.countDataSubscribers, text='200', fg='blue')
        self.cDS200.pack(side='left')
        self.cDS200.bind("<Button-1>", lambda e: (self.cDSSelected.set(200), self.info_fill(Table.Subscribers)))
        Label(self.countDataSubscribers, padx=10, text='Всего:').pack(side='left')
        row = DBAccessor.select_info(fr0m="Subscriber", select="SELECT COUNT(ID)")
        self.cDSTotal = Label(self.countDataSubscribers, fg='red', text=str(row[0][0]))
        self.cDSTotal.pack(side='left')

        Button(self.countDataSubscribers, text='<', width=3,
               command=lambda: self.change_paragraph('<', Table.Subscribers)).pack(
            side='left')
        self.cDSCurrent = IntVar(self.main_menu, 0)
        Label(self.countDataSubscribers, textvariable=self.cDSCurrent).pack(side='left')
        Button(self.countDataSubscribers, text='>', width=3,
               command=lambda: self.change_paragraph('>', Table.Subscribers)).pack(
            side='left')
        self.countDataSubscribers.grid(column=2, row=3)
        # --
        self.countDataEditions = Frame(self.main_window)
        Label(self.countDataEditions, text='Кол-во:').pack(side='left')
        self.cDESelected = IntVar(self.main_menu, 20)
        self.cDE20 = Label(self.countDataEditions, text='20', fg='blue')
        self.cDE20.pack(side='left')
        self.cDE20.bind("<Button-1>", lambda e: (self.cDESelected.set(20), self.info_fill(Table.Editions)))
        self.cDE100 = Label(self.countDataEditions, text='100', fg='blue')
        self.cDE100.pack(side='left')
        self.cDE100.bind("<Button-1>", lambda e: (self.cDESelected.set(100), self.info_fill(Table.Editions)))
        self.cDE200 = Label(self.countDataEditions, text='200', fg='blue')
        self.cDE200.pack(side='left')
        self.cDE200.bind("<Button-1>", lambda e: (self.cDESelected.set(200), self.info_fill(Table.Editions)))
        Label(self.countDataEditions, padx=10, text='Всего:').pack(side='left')
        row = DBAccessor.select_info(fr0m="Edition", select="SELECT COUNT(ID)")
        self.cDETotal = Label(self.countDataEditions, fg='red', text=str(row[0][0]))
        self.cDETotal.pack(side='left')

        Button(self.countDataEditions, text='<', width=3,
               command=lambda: self.change_paragraph('<', Table.Editions)).pack(
            side='left')
        self.cDECurrent = IntVar(self.main_menu, 0)
        Label(self.countDataEditions, textvariable=self.cDECurrent).pack(side='left')
        Button(self.countDataEditions, text='>', width=3,
               command=lambda: self.change_paragraph('>', Table.Editions)).pack(
            side='left')
        self.countDataEditions.grid(column=2, row=6)

        self.info_fill()

        if login is not None:
            login.root.destroy()

        self.main_window.mainloop()

    def trev_select(self, place, event=None):
        if place == Table.Subscribers:
            value = self.tableSubscribers.item(self.tableSubscribers.selection()[0], option='value')
            if value[4] is not None or value[4] != "":
                image_name = value[4]
                if (image_name is None) or (image_name == 'None'):
                    image_name = 'none.png'
                img = Image.open(DBAccessor.base_path + r"photos/subscribers/" + image_name)
                img.thumbnail((225, 225), Image.ANTIALIAS)
                imgScrb = itk.PhotoImage(img, master=self.main_menu)
                self.cnvScrb.delete('all')
                self.cnvScrb.image = imgScrb
                self.cnvScrb.create_image(0, 0, anchor=NW, image=imgScrb)
        elif place == Table.Editions:
            value = self.tableEditions.item(self.tableEditions.selection()[0], option='value')
            if value[3] is not None or value[3] != "":
                image_name = value[3]
                if (image_name is None) or (image_name == 'None'):
                    image_name = 'none.png'
                img = Image.open(DBAccessor.base_path + r"photos/editions/" + image_name)
                img.thumbnail((225, 225), Image.ANTIALIAS)
                imgEdt = itk.PhotoImage(img, master=self.main_menu)
                self.cnvEdt.delete('all')
                self.cnvEdt.image = imgEdt
                self.cnvEdt.create_image(0, 0, anchor=NW, image=imgEdt)

    def change_item(self, type):
        if type == Table.Readings:
            value = self.tableReadings.item(self.tableReadings.selection()[0], option='value')
            UpdateForms.ReadingUpdateForm(value, self)
        elif type == Table.Editions:
            value = self.tableEditions.item(self.tableEditions.selection()[0], option='value')
            UpdateForms.EditionUpdateForm(value, self)
        elif type == Table.Subscribers:
            value = self.tableSubscribers.item(self.tableSubscribers.selection()[0], option='value')
            UpdateForms.SubscriberUpdateForm(value, self)

    def change_paragraph(self, direction, table):
        if table == Table.Readings:
            if direction == '<':
                expected = self.cDRCurrent.get() - self.cDRSelected.get()
                if expected >= 0:
                    self.cDRCurrent.set(expected)
                else:
                    self.cDRCurrent.set(0)
            elif direction == '>':
                expected = self.cDRCurrent.get() + self.cDRSelected.get()
                if expected <= int(self.cDRTotal['text']):
                    self.cDRCurrent.set(expected)
            self.info_fill(Table.Readings)
        elif table == Table.Subscribers:
            if direction == '<':
                expected = self.cDSCurrent.get() - self.cDSSelected.get()
                if expected >= 0:
                    self.cDSCurrent.set(expected)
                else:
                    self.cDSCurrent.set(0)
            elif direction == '>':
                expected = self.cDSCurrent.get() + self.cDSSelected.get()
                if expected <= int(self.cDSTotal['text']):
                    self.cDSCurrent.set(expected)
            self.info_fill(Table.Subscribers)
        elif table == Table.Editions:
            if direction == '<':
                expected = self.cDECurrent.get() - self.cDESelected.get()
                if expected >= 0:
                    self.cDECurrent.set(expected)
                else:
                    self.cDECurrent.set(0)
            elif direction == '>':
                expected = self.cDECurrent.get() + self.cDESelected.get()
                if expected <= int(self.cDETotal['text']):
                    self.cDECurrent.set(expected)
            self.info_fill(Table.Editions)

    def info_fill(self, table: Table = None):
        if table == Table.Readings or table is None:
            self.tableReadings.delete(*self.tableReadings.get_children())
            rows = DBAccessor.select_info(fr0m='vReadings',
                                          where=f'WHERE ID between {self.cDRCurrent.get()} AND {self.cDRCurrent.get() + self.cDRSelected.get()}')
            for row in rows:
                self.tableReadings.insert("", 'end', values=row)
            self.cDRTotal['text'] = str(DBAccessor.select_info(fr0m="Readings", select="SELECT COUNT(ID)")[0][0])

        if table == Table.Editions or table is None:
            self.tableEditions.delete(*self.tableEditions.get_children())
            rows = DBAccessor.select_info(fr0m='Edition',
                                          where=f'WHERE ID between {self.cDECurrent.get()} AND {self.cDECurrent.get() + self.cDESelected.get()}')
            for row in rows:
                self.tableEditions.insert("", 'end', values=row)
            self.cDETotal['text'] = str(DBAccessor.select_info(fr0m="Edition", select="SELECT COUNT(ID)")[0][0])

        if table == Table.Subscribers or table is None:
            self.tableSubscribers.delete(*self.tableSubscribers.get_children())
            rows = DBAccessor.select_info(fr0m='Subscriber',
                                          where=f'WHERE ID between {self.cDSCurrent.get()} AND {self.cDSCurrent.get() + self.cDSSelected.get()}')
            for row in rows:
                self.tableSubscribers.insert("", 'end', values=row)
            self.cDSTotal['text'] = str(DBAccessor.select_info(fr0m="Subscriber", select="SELECT COUNT(ID)")[0][0])

    def treeview_sort_column(self, tv, col, reverse):
        l = [(tv.set(k, col), k) for k in tv.get_children('')]
        l.sort(reverse=reverse)

        # rearrange items in sorted positions
        for index, (val, k) in enumerate(l):
            tv.move(k, '', index)

        # reverse sort next time
        tv.heading(col, command=lambda: \
            self.treeview_sort_column(tv, col, not reverse))

    def open_filter(self, event=None):
        FilterForm.FilterForm(self)

    def begin_filter(self, fr0m, where, type):
        rows = DBAccessor.select_info(fr0m, where)
        if type == 1:
            self.tableEditions.delete(*self.tableEditions.get_children())
            for row in rows:
                self.tableEditions.insert("", "end", values=row)
        elif type == 2:
            self.tableSubscribers.delete(*self.tableSubscribers.get_children())
            for row in rows:
                self.tableSubscribers.insert("", "end", values=row)
        elif type == 3:
            self.tableReadings.delete(*self.tableReadings.get_children())
            for row in rows:
                self.tableReadings.insert("", "end", values=row)

    def new_item(self, type, event=None):
        if type == Table.Readings:
            InsertForms.ReadingInsertForm(self)
        if type == Table.Subscribers:
            InsertForms.SubscriberInsertForm(self)
        if type == Table.Editions:
            InsertForms.EditionInsertForm(self)

    def delete_item(self, type):
        if type == Table.Readings:
            value = self.tableReadings.item(self.tableReadings.selection()[0], option='value')
            answer = messagebox.askyesno("УДАЛЕНИЕ", f'ВНИМАНИЕ!!! Вы ТОЧНО зотите УДАЛИТЬ Запись №{value[0]}???',
                                         master=self.main_window)
            if answer:
                DBAccessor.delete_reading(value[0])
                self.info_fill(Table.Readings)
        elif type == Table.Editions:
            value = self.tableEditions.item(self.tableEditions.selection()[0], option='value')
            answer = messagebox.askyesno("УДАЛЕНИЕ",
                                         f'ВНИМАНИЕ!!! Вы ТОЧНО зотите УДАЛИТЬ ЖУРНАЛ №{value[0]} {value[1]}???',
                                         master=self.main_window)
            if answer:
                DBAccessor.delete_edition(value[0])
                self.info_fill(Table.Editions)
        elif type == Table.Subscribers:
            value = self.tableSubscribers.item(self.tableSubscribers.selection()[0], option='value')
            answer = messagebox.askyesno("УДАЛЕНИЕ",
                                         f'ВНИМАНИЕ!!! Вы ТОЧНО зотите УДАЛИТЬ ЧЕЛОВЕКА(!!!) {value[1]} {value[2]} под номером №{value[0]}???',
                                         master=self.main_window)
            if answer:
                DBAccessor.delete_subscriber(value[0])
                self.info_fill(Table.Subscribers)


if __name__ == '__main__':
    LoginForm()
