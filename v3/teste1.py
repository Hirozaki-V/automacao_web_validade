from tkinter import *
from tkinter.tix import *


class Janela:
    def __init__(self, master=None):
        self.firstContainer = Frame(bd=1, relief='solid')
        self.firstContainer.pack()

        tip = Balloon(root)
        self.help = Button(self.firstContainer, text="i")
        self.help.grid(row=0, column=2)

        self.button = Label(self.firstContainer, text="Help")
        self.button.grid(row=1, column=0)
        self.teste = Entry(self.firstContainer)
        self.teste.grid(row=1, column=1)

        tip.bind_widget(self.button, balloonmsg="Isso é um botão")


root = Tk()
root.geometry('500x300')
Janela(root)
root.mainloop()
