from files.ChessGUI import ChessGUI
from files.logic import game_loop

if __name__ == "__main__":
    gui = ChessGUI()
    game_loop(gui)