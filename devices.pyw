import sqlite3
import webbrowser
from tasks import TasksWindow
from modal import Modal
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from sql_utils import (get_devices_list, get_device_status,
                       toggle_status, del_device, del_task, backup)


class DeviceWindow(ttk.Frame):
    def __init__(self, master=None):
        super().__init__(master, padding=2)
        self.key = "1"
        self.pack(expand=True, fill=BOTH)
        self.guard()

    def guard(self):
        self.guard_frame = Frame(self)
        self.guard_frame.pack()
        self.label = Label(self.guard_frame, text="Введите пароль")
        self.label.pack(side=LEFT)
        self.entry = Entry(self.guard_frame, show="*")
        self.entry.pack(side=LEFT)
        self.button = Button(self.guard_frame, text="Ввести")
        self.button.pack(side=RIGHT)
        self.entry.focus()

        def verify(e):
            if self.entry.get() == self.key:
                self.guard_frame.destroy()
                self.create_variables()
                self.create_widgets()
                self.create_bindings()
                self.fill_devices()
                self.master.resizable(0, 0)
                self.screen_place()
            else:
                messagebox.showinfo("Информация", "Неправильно!")
                self.master.destroy()
        self.button.bind("<Button-1>", verify)
        self.entry.bind("<Return>", verify)

    def screen_place(self):
        w = 800
        h = 600
        sw = (self.winfo_screenwidth()/2)-(w/2)
        sh = (self.winfo_screenheight()/2)-(h/2)
        self.master.geometry("{}x{}+{}+{}".format(w, h, int(sw), int(sh)))

    def fill_devices(self):
        if self.dev_list.size() > 0:
            self.dev_list.delete(0, END)
        names, self.d_ids = get_devices_list()
        for i in names:
            self.dev_list.insert(END, i)

    def create_variables(self):
        self.d_id = None

    def create_widgets(self):
        self.dev_frame = ttk.LabelFrame(
            self,
            text="Выбор анализатора",
            borderwidth=5,
            width=200,
            height=200,
            relief=RIDGE
        )
        self.dev_frame.pack(side=LEFT, expand=False, fill=BOTH)
        self.toplabel = ttk.Label(self.dev_frame, text="Анализаторы:")
        self.toplabel.pack(pady=(5, 0))
        self.dev_list = Listbox(self.dev_frame)
        self.dev_list.pack(expand=True, fill=BOTH)
        self.butt_frame = ttk.LabelFrame(self.dev_frame, text="...")
        self.butt_frame.pack(expand=False, fill=X)
        self.add_button = ttk.Button(self.butt_frame, text="+", width=3)
        self.add_button.pack(side=LEFT)
        self.edit_button = ttk.Button(self.butt_frame, text="...", width=3)
        self.edit_button.pack(side=LEFT)
        self.delete_button = ttk.Button(self.butt_frame, text="X", width=3)
        self.delete_button.pack(side=LEFT)

        self.info_frame = ttk.LabelFrame(
            self,
            text="Доп.Информация",
            borderwidth=5,
            width=200,
            height=400,
            relief=RIDGE
        )
        self.info_frame.pack(side=RIGHT, expand=True, fill=BOTH)
        ###
        self.status_frame = LabelFrame(
            self.info_frame,
            text="Статус",
            padx=20,
            pady=10
        )
        self.status_frame.pack(fill=X)
        self.stat_label = ttk.Label(
            self.status_frame,
            text="Текущее состояние:",
        )
        self.stat_label.pack(side=LEFT)
        self.status = ttk.Label(self.status_frame, text="-")
        self.status.pack(side=LEFT)
        self.toggle_button = ttk.Button(
            self.status_frame,
            text="Перекл. статус",
        )
        self.toggle_button.pack(side=RIGHT)
        self.info_frame = LabelFrame(
            self.info_frame,
            text="Дополнительно",
            padx=20,
            pady=10,
        )
        self.info_frame.pack(fill=X)
        self.info_button = ttk.Button(self.info_frame, text="Задачи")
        self.info_button.pack(side=LEFT)
        self.stock_button = ttk.Button(
            self.info_frame,
            text="Запасные части",
        )
        self.stock_button.pack(side=LEFT)
        self.backup_button = ttk.Button(
            self.info_frame,
            text="Скопировать базу",
        )
        self.backup_button.pack(side=RIGHT)
        self.open_taskify_button = ttk.Button(
            self.info_frame,
            text="Предложения",
        )
        self.open_taskify_button.pack(side=RIGHT)

    def create_bindings(self):
        self.dev_list.bind("<Button-1>", self.handle_device_click)
        self.info_button.bind("<Button-1>", self.open_tasks)
        self.add_button.bind("<Button-1>", self.handle_add_an)
        self.edit_button.bind("<Button-1>", self.handle_edit_an)
        self.delete_button.bind("<Button-1>", self.handle_delete_an)
        self.toggle_button.bind("<Button-1>", self.handle_toggle_button)
        self.backup_button.bind("<Button-1>", self.backup_handler)
        self.open_taskify_button.bind("<Button-1>", self.open_taskify)

    def handle_add_an(self, e):
        dialog = Toplevel()
        a_d = Modal(
            dialog,
            role="add",
            table="devices",
            parent=self
        ).pack()
        dialog.mainloop()

    def handle_edit_an(self, e):
        if self.d_id:
            dialog = Toplevel()
            a_d = Modal(
                dialog,
                role="edit",
                table="devices",
                d_id=self.d_id,
                parent=self
            ).pack()
            dialog.mainloop()

    def handle_delete_an(self, e):
        if self.d_id:
            dialog = Toplevel()
            a_d = Modal(
                dialog,
                role="delete",
                table="devices",
                d_id=self.d_id,
                parent=self
            ).pack()
            dialog.mainloop()

    def handle_device_click(self, e):
        if e.widget.size() > 0:
            i = e.widget.nearest(e.y)
            self.d_id = self.d_ids[i]
            s = get_device_status(self.d_id)
            self.status.config(text=s)
        else:
            self.d_id = None

    def handle_toggle_button(self, e):
        if self.d_id:
            status = self.status["text"]
            if status == "Работает":
                status = "Не работает"
            else:
                status = "Работает"
            toggle_status(self.d_id, status)
            self.status.config(text=status)

    def open_tasks(self, e):
        if self.d_id:
            tasks = Toplevel()
            tasks.title = "Информация"
            tasks_window = TasksWindow(self.d_id, master=tasks)
            tasks_window.mainloop()
        else:
            messagebox.showinfo("Информация", "Выберите анализатор!")

    def open_taskify(self, e):
        webbrowser.open('http://www.taskify.us/2fc70f0580', new=2)

    def backup_handler(self, e):
        result = backup()
        if result:
            messagebox.showinfo(
                "Информация",
                "Копирование базы успешно завершено!",
            )
        else:
            messagebox.showinfo("Информация", "Ошибка копирования!")


if __name__ == "__main__":
    app = DeviceWindow()
    app.master.title("Анализаторы")
    app.mainloop()
