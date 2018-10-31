from tkinter import *
from tkinter import ttk
from sql_utils import *


class Modal(ttk.Frame):
    def __init__(
        self,
        master=None,
        role=None,
        table=None,
        d_id=None,
        t_id=None,
        parent=None
    ):
        super().__init__(master, padding=2)
        self.pack()
        self.role = role
        self.parent = parent
        self.d_id = d_id
        self.t_id = t_id
        self.table = table
        self.create_widgets()
        self.focus()
    
    def focus(self):
        if self.role != "delete":
            self.entry.focus_force()
        
    def create_sql(self):
        if self.role == "add":
            if self.d_id:
                sql = "insert into {}(title,d_id,comment) values(?,'{}', '')".format(
                    self.table,
                    self.d_id
                )
                return sql
            else:
                sql = """
                    insert into
                    {}(name,status)
                    values(?,'Работает')
                """.format(self.table)

                return sql
        elif self.role == "edit":
            if self.d_id:
                sql = """
                    update {}
                    set name=?
                    where id={}
                """.format(self.table, self.d_id)

                return sql
            elif self.t_id:
                sql = """
                    update {}
                    set title=?
                    where id={}
                """.format(self.table, self.t_id)
                return sql
        elif self.role == "delete":
            if self.d_id:
                sql = """
                    delete from {}
                    where id={}
                """.format(self.table, self.d_id)
                return sql
            elif self.t_id:
                sql = """
                    delete from {}
                    where id={}
                """.format(self.table, self.t_id)
                return sql

    def create_widgets(self):
        self.label = ttk.Label(self, text="Введите текст")
        self.buttons_frame = Frame(self)

        if self.role is "add":
            self.yes_button = ttk.Button(self.buttons_frame, text="Добавить")
            self.yes_button.bind("<Button-1>", self.add_handler)
        elif self.role is "edit":
            self.yes_button = ttk.Button(self.buttons_frame, text="Изменить")
            self.yes_button.bind("<Button-1>", self.edit_handler)
        elif self.role is "delete":
            self.label = ttk.Label(self, text="Удалить элемент?")
            self.yes_button = ttk.Button(self.buttons_frame, text="Удалить")
            self.yes_button.bind("<Button-1>", self.delete_handler)
        else:
            self.destroy()
            return None
        self.no_button = ttk.Button(self.buttons_frame, text="Отмена")
        self.no_button.bind("<Button>", self.cancel_handler)
        self.label.pack()
        if self.role is not "delete":
            self.entry = ttk.Entry(self)
            self.entry.pack()
        self.buttons_frame.pack()
        self.yes_button.pack(side=LEFT)
        self.no_button.pack(side=LEFT)

    def add_handler(self, e):
        print("=>handling add")
        sql = self.create_sql()
        value = self.entry.get()
        if value:
            add(value, sql)
        if self.table == "tasks":
            self.parent.fill_tasks(self.d_id)
        else:
            self.parent.fill_devices()
        self.master.destroy()

    def edit_handler(self, e):
        sql = self.create_sql()
        value = self.entry.get()
        if value:
            edit(value, sql)
        if self.table == "tasks":
            self.parent.fill_tasks(self.parent.d_id)
        else:
            self.parent.fill_devices()
        self.master.destroy()

    def delete_handler(self, e):
        sql = self.create_sql()
        if self.table == "tasks":
            delete(sql)
            self.parent.fill_tasks(self.parent.d_id)
        else:
            t_ids = get_tasks_list(self.d_id)[1]
            del_task(self.d_id)
            delete(sql)
            self.parent.fill_devices()
        self.master.destroy()

    def cancel_handler(self, e):
        self.master.destroy()


if __name__ == "__main__":
    root = Tk()
    app = Modal(root, role="delete", table="deveic", d_id=1, parent=None)
    root.mainloop()
