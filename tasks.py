import datetime
from tkinter import *
from tkinter import ttk, messagebox
from modal import Modal
from sql_utils import (get_tasks_list,
get_comments,update_comment,del_task,)


class TasksWindow(ttk.Frame):
    def __init__(self, d_id, master=None):
        super().__init__(master, padding=2)
        self.d_id = d_id
        self.pack(expand=True, fill=BOTH)
        self.create_variables()
        self.create_widgets()
        self.create_bindings()
        self.fill_tasks(d_id)
        self.master.resizable(0, 0)
        self.screen_place()
        
    def screen_place(self):
        w = 800
        h = 600
        sw = (self.winfo_screenwidth()/2)-(w/2)
        sh = (self.winfo_screenheight()/2)-(h/2)
        self.master.geometry("{}x{}+{}+{}".format(w, h, int(sw), int(sh)))

    def fill_tasks(self, index):
        if self.tasks_list.size() > 0:
            self.tasks_list.delete(0, END)
        tasks, self.task_ids = get_tasks_list(index)
        print("=>got tasks")
        for i in tasks:
            self.tasks_list.insert(END, i)
        self.comments_field.delete('1.0', END)

    def fill_comments(self, index):
        self.comments_field.delete('1.0', END)
        comments = get_comments(self.t_id)
        print("=>got comments", index)
        self.comments_field.insert(END, comments)

    def create_variables(self):
        self.t_id = None

    def create_bindings(self):
        self.tasks_list.bind("<Button-1>", self.handle_task_click)
        self.add_task.bind("<Button-1>",  self.handle_add_task)
        self.edit_task.bind("<Button-1>", self.handle_edit_task)
        self.delete_task.bind("<Button-1>", self.handle_delete_task)
        self.update_button.bind("<Button-1>", self.handle_update_comment)
        self.add_date_button.bind("<Button-1>", self.add_date)

    def create_widgets(self):
        self.tasks_frame = ttk.LabelFrame(
            self,
            text="Задачи",
            borderwidth=5,
            width=300,
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
        self.add_task = ttk.Button(self.task_butt_frame, text="+", width=3)
        self.add_task.pack(side=LEFT)
        self.edit_task = ttk.Button(self.task_butt_frame, text="...", width=3)
        self.edit_task.pack(side=LEFT)
        self.delete_task = ttk.Button(self.task_butt_frame, text="X", width=3)
        self.delete_task.pack(side=LEFT)

        self.comments_frame = ttk.LabelFrame(
            self,
            text="Комментарии",
            borderwidth=5,
            width=100,
            relief=RIDGE
        )
        self.comments_frame.pack(side=RIGHT, expand=True, fill=BOTH)
        self.comments_field = Text(self.comments_frame)
        self.comments_field.pack(expand=True, fill=BOTH)
        self.comm_butt_frame = ttk.LabelFrame(
            self.comments_frame,
            text="inner frame"
        )
        self.comm_butt_frame.pack()
        self.update_button = ttk.Button(self.comm_butt_frame, text="Обновить")
        self.update_button.pack(side=LEFT)
        self.add_date_button = ttk.Button(self.comm_butt_frame, text="Добавить дату")
        self.add_date_button.pack(side=RIGHT)

    def handle_task_click(self, e):
        w = e.widget
        if w.size() > 0:
            i = w.nearest(e.y)
            self.t_id = self.task_ids[i]
            self.fill_comments(self.t_id)

    def handle_add_task(self, e):
        dialog = Toplevel()
        a_t = Modal(
            dialog,
            role="add",
            table="tasks",
            d_id=self.d_id,
            parent=self
        )
        dialog.mainloop()

    def handle_edit_task(self, e):
        if self.t_id:
            dialog = Toplevel()
            e_t = Modal(
                dialog,
                role="edit",
                table="tasks",
                t_id=self.t_id,
                parent=self
            )
            dialog.mainloop()
        else:
            messagebox.showinfo("Информация", "Выберите задачу")
        

    def handle_delete_task(self, e):
        if self.t_id:
            dialog = Toplevel()
            d_t = Modal(
                dialog,
                role="delete",
                table="tasks",
                t_id=self.t_id,
                parent=self
            )
            dialog.mainloop()
        else:
            messagebox.showinfo("Информация", "Выберите задачу")

    def handle_update_comment(self, e):
        if self.t_id:
            update_comment(self.t_id,self.comments_field.get("1.0",END))
    
    def add_date(self, e):
        date = "\n- "+datetime.datetime.now().strftime("%d.%m.%Y")+" -\n"
        self.comments_field.insert(END, date)

if __name__ == "__main__":
    app = TasksWindow(5)
    app.mainloop()
