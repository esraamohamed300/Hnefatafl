import tkinter as tk
from GUI.controls import HomePage, SettingsPage
from GUI.board_gui import BoardGUI


class GameWindow:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Hnefatafl — Viking Chess")
        self.root.configure(bg="#1a1208")
        self.root.resizable(True, True)

        self.current_frame = None
        self._show_home()

    # ── navigation ────────────────────────────────────────────────────────────
    def _clear(self):
        """Destroy the current page before showing a new one."""
        if self.current_frame:
            self.current_frame.destroy()
            self.current_frame = None

    def _show_home(self):
        self._clear()
        frame = HomePage(
            parent      = self.root,
            on_new_game = self._show_settings
        )
        frame.pack(expand=True, fill="both")
        self.current_frame = frame

        # fix window size for home page
        self.root.geometry("560x540")
        self._center()

    def _show_settings(self):
        self._clear()
        frame = SettingsPage(
            parent        = self.root,
            on_start_game = self._start_game,
            on_back       = self._show_home
        )
        frame.pack(expand=True, fill="both")
        self.current_frame = frame

        # fix window size for settings page
        self.root.geometry("560x580")
        self._center()

    def _start_game(self, mode, side, difficulty):
        self._clear()
        frame = BoardGUI(
            parent      = self.root,
            mode        = mode,
            human_side  = side,
            difficulty  = difficulty,
            on_end_game = self._show_home
        )
        frame.pack(expand=True, fill="both")
        self.current_frame = frame

        # fix window size for game board
        self.root.geometry("698x760")
        self._center()

    # ── center window on screen ───────────────────────────────────────────────
    def _center(self):
        self.root.update_idletasks()
        w = self.root.winfo_width()
        h = self.root.winfo_height()
        x = (self.root.winfo_screenwidth()  // 2) - (w // 2)
        y = (self.root.winfo_screenheight() // 2) - (h // 2)
        self.root.geometry(f"{w}x{h}+{x}+{y}")

    # ── run ───────────────────────────────────────────────────────────────────
    def run(self):
        self.root.mainloop()