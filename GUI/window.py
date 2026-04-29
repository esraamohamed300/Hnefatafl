import tkinter as tk
from GUI.board_gui import BoardGUI

class GameWindow:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Hnefatafl")

        self.board_gui = BoardGUI(self.root)

    def run(self):
        self.root.mainloop()