import sqlite3 as sql
# import os

base_path = r"E:\Работа(ы) по 0101110\PressAgency\\"


# base_path = "".join(os.path.abspath("")) + '\\'
# Thx PyCharm for this


def intTryParse(value):
    try:
        return int(value), True
    except ValueError:
        return value, False


try:
    conn = sql.connect("AgencyDB.db")
except:
    conn = sql.connect(base_path + "AgencyDB.db")
cur = conn.cursor()


def select_info(fr0m: str, where: str = None, order: str = None, select: str = None):
    if select is None:
        command = "Select * FROM " + fr0m
    else:
        command = select + " FROM " + fr0m

    if where is not None:
        command = command + " " + where
    if order is not None:
        command = command + " " + order
    cur.execute(command)
    rows = cur.fetchall()
    return rows


def insert_reading(values):
    cur.execute(f"INSERT INTO Readings VALUES (?,?,?,?)", values)
    conn.commit()


def insert_edition(values):
    cur.execute(f"INSERT INTO Edition(ID, Name, Cost) VALUES (?,?,?)", values)
    conn.commit()


def insert_subscriber(values):
    cur.execute(f"INSERT INTO Subscriber(ID, Name, Surname, Gender) VALUES (?,?,?,?)", values)
    conn.commit()


def update_reading(old_id, values):
    cur.execute('UPDATE Readings SET ID = ?, ID_Subscriber = ?, ID_Edition = ?, Sub_Term = ? '
                f'WHERE ID = {old_id}', values)
    conn.commit()


def update_edition(old_id, values):
    cur.execute('UPDATE Edition SET ID = ?, Name = ?, Cost = ?, Photo = ? '
                f'WHERE ID = {old_id}', values)
    conn.commit()


def update_subscriber(old_id, values):
    cur.execute('Update Subscriber SET ID = ?, Name = ?, Surname = ?, Gender = ?, Photo = ?'
                f'WHERE ID = {old_id}', values)
    conn.commit()


def delete_reading(id):
    cur.execute(f'DELETE FROM Readings WHERE ID = {id}')
    conn.commit()


def delete_edition(id):
    cur.execute(f'DELETE FROM Edition WHERE ID = {id}')
    conn.commit()


def delete_subscriber(id):
    cur.execute(f'DELETE FROM Subscriber WHERE ID = {id}')
    conn.commit()
