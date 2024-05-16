#!/usr/bin/python3
import pathlib
import tkinter as tk
import pygubu
import os

#IN-HOUSE IMPORTS
import restaurant_frontend
import  customer_frontend

PROJECT_PATH = pathlib.Path(__file__).parent
PROJECT_UI = PROJECT_PATH / "main_gui.ui"

class MainGuiApp:
    def __init__(self, master=None):
        self.builder = builder = pygubu.Builder()
        builder.add_resource_path(PROJECT_PATH)
        builder.add_from_file(PROJECT_UI)
        # Main widget
        self.mainwindow: ttk.Frame = builder.get_object("frame1", master)
        builder.connect_callbacks(self)

    def run(self):
        self.mainwindow.mainloop()

    def e_open_staff(self):
        restaurant_frontend.run()

    def e_open_customer(self):
        customer_frontend.run()

if __name__ == "__main__":
    root = tk.Tk()
    app = MainGuiApp(root)
    app.run()
