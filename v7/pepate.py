from tkinter import *
from tkinter import ttk
from time import sleep


class Waiting:
    def __init__(self, master=None):
        self.firstContainer = Frame()
        self.firstContainer.pack()
        label = Label(self.firstContainer, text="Waiting...")
        label["font"] = "Arial 50 bold"
        label.pack(pady=150)

        pro = ttk.Progressbar(self.firstContainer, orient=HORIZONTAL, mode="determinate", length=900)
        pro.pack(side=BOTTOM)
        t = 0
        while t < 100:
            pro['value'] += 20
            root.update_idletasks()
            t += 20
            sleep(0.5)
        else:
            root.after(100, self.task)

    def task(self):
        sleep(2)
        root.destroy()
        Janela().mainloop()


class Janela(Tk):
    def __init__(self, master=None):
        super().__init__()


def center(win):
    win.update_idletasks()
    width = 900# win.winfo_width()
    height = 400# win.winfo_height()
    x = int((win.winfo_screenwidth() / 2) - (width / 2))
    y = int((win.winfo_screenheight() / 2) - (height / 2))
    return f"{width}x{height}+{x}+{y}"


root = Tk()
root.geometry(center(root))
root.overrideredirect(True)
Waiting(root)
root.mainloop()

