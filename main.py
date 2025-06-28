from files.ChessGUI import ChessGUI
from files.images import image_editor


if __name__ == "__main__":
    while True:
        try:
            windowsize = int(input("\nBitte Fenstergrösse angeben(in px): "))
            if windowsize >= 50 and windowsize <= 2000:
                break
            else:
                print("\nBitte eine Zahl zwischen 50 und 2000.")
        except ValueError:
            print("\nBitte Zahl angeben! (zwischen 50 und 2000)")
    editor = image_editor(windowsize)
    editor.create_copys()
    editor.resize()

    gui = ChessGUI(windowsize)
    gui.run()