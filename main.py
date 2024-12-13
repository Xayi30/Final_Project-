import tkinter as tk
from data_manager import DataManager
from atm_gui import ATMApp

if __name__ == "__main__":
    data_manager = DataManager("accounts.json")
    root = tk.Tk()
    app = ATMApp(root, data_manager)
    root.mainloop()
