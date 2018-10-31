from tkinter import *
from tkinter import ttk, messagebox
from modal import Modal
from sql_utils import (get_tasks_list,
get_comments,update_comment,del_task,get_archived_tasks, get_archived_task)

class ArchivedTasksWindow(ttk.Frame):
    def __init__(self, parent, master=None):
        super().__init__(master, padding=2)
        self.parent = parent
        self.pack(expand=True, fill=BOTH)
        self.create_variables()
        self.create_widgets()
        self.create_bindings()
        self.fill_tasks()
        self.master.resizable(0, 0)
        self.screen_place()
        
    def screen_place(self):
        w = 400
        h = 600
        sw = (self.winfo_screenwidth()/2)-(w/2)
        sh = (self.winfo_screenheight()/2)-(h/2)
        self.master.geometry("{}x{}+{}+{}".format(w, h, int(sw), int(sh)))

    def fill_tasks(self):
        if self.tasks_list.size() > 0:
            self.tasks_list.delete(0, END)
        tasks, self.task_ids = get_archived_tasks()
        print("=>got tasks")
        for i in tasks:
            self.tasks_list.insert(END, i)

    def create_variables(self):
        self.t_id = None

    def create_bindings(self):
        self.tasks_list.bind("<Button-1>", self.handle_task_click)
        self.restore_task.bind("<Button-1>",  self.handle_restore_task)
        self.delete_task.bind("<Button-1>", self.handle_delete_task)

    def create_widgets(self):
        self.tasks_frame = ttk.LabelFrame(
            self,
            text="Архивные Задачи",
            borderwidth=5,
            width=400,
            relief=RIDGE
        )
        self.tasks_frame.pack(side=LEFT, fill=BOTH)
        self.tasks_frame.pack_propagate(0)

        self.tasks_list = Listbox(self.tasks_frame)
        self.tasks_list.pack(expand=True, fill=BOTH)
        self.task_butt_frame = ttk.LabelFrame(
            self.tasks_frame,
            text="inner frame"
        )
        self.task_butt_frame.pack()
        self.restore_task = ttk.Button(self.task_butt_frame, text="Восстановить")
        self.restore_task.pack(side=LEFT)
        self.delete_task = ttk.Button(self.task_butt_frame, text="Удалить")
        self.delete_task.pack(side=LEFT)

    def handle_task_click(self, e):
        w = e.widget
        if w.size() > 0:
            i = w.nearest(e.y)
            self.t_id = self.task_ids[i]

    def handle_restore_task(self, e):
        if self.t_id:
            values = get_archived_task(self.t_id)
            sql = "insert into tasks(d_id,title,comment) values(?,?,?,?)"
            add(values, sql)
            self.parent.fill_task()
            del_sql = "delete from archived_tasks where id = {}".format(self.t_id)
            delete(del_sql)
            self.fill_tasks()
        else:
            messagebox.showinfo("Информация", "Выберите задачу")

    def handle_delete_task(self, e):
        if self.t_id:
            dialog = Toplevel()
            d_t = Modal(
                dialog,
                role="delete",
                table="archived_tasks",
                t_id=self.t_id,
                parent=self
            )
            dialog.mainloop()
        else:
            messagebox.showinfo("Информация", "Выберите задачу")


if __name__ == "__main__":
    app = ArchivedTasksWindow(None)
    app.mainloop()