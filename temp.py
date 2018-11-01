from tkinter import *
from tkinter import ttk

class Example(ttk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.pack()
        self.create_layout()
        self.screen_place()
    
    def create_layout(self):
        self.comment = Text(self, height=5)
        self.comment.pack()
        self.b = ttk.Button(self, text="print")
        self.b.pack()
        self.b.bind("<Button-1>", self.print_info)
    
    def print_info(self,e):
        print(self.comment.get("1.0",END))
    
    def screen_place(self):
        w = 300
        h = 300
        sw = (self.winfo_screenwidth()/2)-(w/2)
        sh = (self.winfo_screenheight()/2)-(h/2)
        self.master.geometry("{}x{}+{}+{}".format(w, h, int(sw), int(sh)))

if __name__ == "__main__":
    app = Example()
    app.mainloop()
