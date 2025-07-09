from tkinter import *
from tkinter import ttk
import threading
import os
import webbrowser
from ttkthemes import ThemedStyle
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
        self.darkmodestate = IntVar()

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

        self.label = ttk.Label(self.frm, text="Schach Menu", anchor="center")
        self.label.grid(column=0, row=0, columnspan=5, sticky="nsew")

        self.entry = ttk.Entry(self.frm)
        self.entry.grid(column=1, row=4, sticky="nsew")

        self.quitbutton = ttk.Button(self.frm, text="Start Game!", command=self.thread_startgame)
        self.quitbutton.grid(column=3, row=6, sticky="nsew")

        self.option1 = ttk.Radiobutton(self.frm, value=0, variable=self.selected_option, text="600px (empfohlen)")
        self.option1.grid(column=0, row=1, sticky="nsew")

        self.option2 = ttk.Radiobutton(self.frm, variable=self.selected_option, value=1, text="800px")
        self.option2.grid(column=0, row=2, sticky="nsew")

        self.option3 = ttk.Radiobutton(self.frm, variable=self.selected_option, value=2, text="400px")
        self.option3.grid(column=0, row=3, sticky="nsew")

        self.option4 = ttk.Radiobutton(self.frm, variable=self.selected_option, value=3, text="eigene (in px)")
        self.option4.grid(column=0, row=4, sticky="nsew")

        self.darkmode = ttk.Checkbutton(self.frm, text="Dunkel", variable=self.darkmodestate, command=self.turn_to_the_dark)
        self.darkmode.grid(column=0, row=6)

        self.combobox = ttk.Combobox(self.frm)
        self.combobox["values"] = ("Klassisch",
                                   "Klassisch 2",
                                   "Grau",
                                   "Grau 2",
                                   "Grau 3",
                                   "Grau 4",
                                   "Grün",
                                   "Gold",
                                   "Pink",
                                   "Blau",
                                   "Violett",
                                   "Rot",
                                   "Vanilla")
        self.combobox.grid(column=3, row=2)

        self.turn_to_the_dark()

        self.root.mainloop()

    def thread_startgame(self):
        ori_color = self.combobox.get()
        print(ori_color)
        if ori_color == "" or ori_color == "Klassisch":
            color = "classic1"
        elif ori_color == "Klassisch 2":
            color = "classic2"
        elif ori_color == "Grau":
            color = "gray1"
        elif ori_color == "Grau 2":
            color = "gray2"
        elif ori_color == "Grau 3":
            color = "gray3"
        elif ori_color == "Grau 4":
            color = "gray4"
        elif ori_color == "Grün":
            color = "green1"
        elif ori_color == "Gold":
            color = "gold1"
        elif ori_color == "Pink":
            color = "pink1"
        elif ori_color == "Blau":
            color = "blue1"
        elif ori_color == "Violett":
            color = "violet1"
        elif ori_color == "Rot":
            color = "red1"
        elif ori_color == "Vanilla":
            color = "vanilla1"

        value = self.selected_option.get()
        if value == 0:
            threading.Thread(target=self.run_game(600, color, self.darkmodestate.get())).start()
        elif value == 1:
            threading.Thread(target=self.run_game(800, color, self.darkmodestate.get())).start()
        elif value == 2:
            threading.Thread(target=self.run_game(400, color, self.darkmodestate.get())).start()
        else:
            try:
                size = int(round(float(self.entry.get()), 1))
            except ValueError:
                print("Only Numbers")
                return
            if size < 50:
                return
            if size > 2000:
                return
            threading.Thread(target=self.run_game(size, color, self.darkmodestate.get())).start()

    def run_game(self, windowsize, boardcolor, darkmode):
        self.editor = image_editor(windowsize)
        self.editor.create_copys()
        self.editor.resize()
        self.chess_gui = ChessGUI(windowsize, boardcolor, self.editor.path, darkmode=darkmode)
        self.chess_gui.run()

    def turn_to_the_dark(self):
        if self.darkmodestate.get() == 1:
            children_list = self.all_children()
            for i in children_list:
                style = ThemedStyle(i)
            style.set_theme("equilux")
        else:
            children_list = self.all_children()
            for i in children_list:
                style = ThemedStyle(i)
            style.set_theme("arc")

    def all_children (self) :
        _list = self.root.winfo_children()

        for item in _list :
            if item.winfo_children() :
                _list.extend(item.winfo_children())
        
        return _list
    
if __name__ == "__main__":
    gui = StartGUI()