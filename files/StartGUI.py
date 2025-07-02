from tkinter import *
from tkinter import ttk
import threading
import os
import webbrowser
if __name__ != "__main__":
    from .ChessGUI import ChessGUI
    from .images import image_editor




class StartGUI:
    def __init__(self):
        self.rows = 8
        self.columns = 5
        self.root = Tk()
        self.root.title("Start")
        self.root.geometry("450x450")
        self.root.rowconfigure(0, weight=1)
        self.root.columnconfigure(0, weight=1)

        self.icon = PhotoImage(file = f"{os.path.join(os.path.dirname(__file__), 'icon.png')}")
        self.root.iconphoto(True, self.icon)

        self.selected_option = IntVar()

        self.frm = ttk.Frame(self.root)
        self.frm.grid(row=0, column=0, sticky="nsew")

        for i in range(self.rows):
            self.frm.rowconfigure(i, weight=1)
        for i in range(self.columns):
            self.frm.columnconfigure(i, weight=1)

        self.menu = Menu(self.root)
        self.root.config(menu=self.menu)

        self.help_menu = Menu(self.menu, tearoff=0)
        self.help_menu.add_command(label="GitHub",command=lambda: webbrowser.open('https://github.com/M3M0KA/PyChess', autoraise=True))

        self.menu.add_cascade(label="Hilfe", menu=self.help_menu)

        self.label = Label(self.frm, text="Schach Menu")
        self.label.grid(column=0, row=0, columnspan=5, sticky="nsew")

        self.entry = Entry(self.frm)
        self.entry.grid(column=1, row=4, sticky="nsew")

        self.quitbutton = Button(self.frm, text="Start Game!", command=self.thread_startgame)
        self.quitbutton.grid(column=3, row=6, sticky="nsew")

        self.option1 = Radiobutton(self.frm, value=0, variable=self.selected_option, text="600px (empfohlen)")
        self.option1.grid(column=0, row=1, sticky="nsew")

        self.option2 = Radiobutton(self.frm, variable=self.selected_option, value=1, text="800px")
        self.option2.grid(column=0, row=2, sticky="nsew")

        self.option3 = Radiobutton(self.frm, variable=self.selected_option, value=2, text="400px")
        self.option3.grid(column=0, row=3, sticky="nsew")

        self.option4 = Radiobutton(self.frm, variable=self.selected_option, value=3, text="eigene (in px)")
        self.option4.grid(column=0, row=4, sticky="nsew")

        self.root.mainloop()

    def thread_startgame(self):
        value = self.selected_option.get()
        if value == 0:
            threading.Thread(target=self.run_game(600)).start()
        elif value == 1:
            threading.Thread(target=self.run_game(800)).start()
        elif value == 2:
            threading.Thread(target=self.run_game(400)).start()
        else:
            try:
                size = int(self.entry.get())
            except TypeError:
                print("Only Numbers")
                return
            if size <= 50:
                return
            if size >= 2000:
                return
            threading.Thread(target=self.run_game(size)).start()

    def run_game(self, windowsize):
        self.editor = image_editor(windowsize)
        self.editor.create_copys()
        self.editor.resize()
        self.chess_gui = ChessGUI(windowsize)
        self.chess_gui.run()

if __name__ == "__main__":
    gui = StartGUI()