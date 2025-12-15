# main.py
import sys
import os
import tkinter as tk

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))

from app.urm import URMExecutorGUI

if __name__ == "__main__":
    root = tk.Tk()
    app = URMExecutorGUI(root)
    root.mainloop()
