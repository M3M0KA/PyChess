from files.ChessGUI import ChessGUI
from files.images import image_editor


if __name__ == "__main__":
    while True:
        try:
            windowsize = input("\nBitte Fenstergrösse angeben(in px): ")
            windowsize1 = int(windowsize)
            if windowsize1 >= 50 and windowsize1 <= 2000:
                break
            else:
                print("\nBitte eine Zahl zwischen 50 und 2000.")
        except ValueError:
            if windowsize == "":
                windowsize1 = 500
                break
            print("\nBitte Zahl angeben! (zwischen 50 und 2000)")
    editor = image_editor(windowsize1)
    editor.create_copys()
    editor.resize()

    gui = ChessGUI(windowsize1)
    gui.run()