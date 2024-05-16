#!/usr/bin/python3
import pathlib
import tkinter as tk
import pygubu
import sqlhandler

PROJECT_PATH = pathlib.Path(__file__).parent
PROJECT_UI = PROJECT_PATH / "restaurant_gui.ui"


class RestaurantGuiApp:
    def __init__(self, master=None):
        self.builder = builder = pygubu.Builder()
        builder.add_resource_path(PROJECT_PATH)
        builder.add_from_file(PROJECT_UI)
        # Main widget
        self.mainwindow: ttk.Frame = builder.get_object("frame1", master)

        self.var_order_id_entry: tk.IntVar = None
        builder.import_variables(self)

        builder.connect_callbacks(self)

    def run(self):
        self.orders_database = sqlhandler.RestaurantDatabase()
        self.refresh_orders()

        self.mainwindow.mainloop()

    #################
    # --> GETTERS <--
    #################
    
    def get_entry(self, entry_name : str):
        ret : tk.Entry = self.builder.get_object(entry_name)
        return ret
    
    def get_textbox(self, textbox_name : str):
        ret : tk.Text = self.builder.get_object(textbox_name)
        return ret
    
    def get_button(self, button_name : str):
        ret : tk.Button = self.builder.get_object(button_name)
        return ret
    
    ##########################
    #--> UTILITY FUNCTIONS <--
    ##########################
    
    def refresh_orders(self):
        self.clean_textbox("w_orders_textbox")
        for order in self.orders_database.return_all_orders():
            self.append_to_textbox("w_orders_textbox", f"ID: {order[0]}\n---->NAME: {order[1]}\n---->TYPE: {order[2]}\n---->ORDER: {order[3]}\n---->ADDRESS: {order[4]}\n---->TABLE: {order[5]}\n---->TOTAL: {order[6]}$\n")

    def clean_textbox(self, textbox : str):
        self.get_textbox(textbox).configure(state="normal")
        self.get_textbox(textbox).delete("1.0", tk.END)
        self.get_textbox(textbox).configure(state="disabled")

    def append_to_textbox(self, textbox : str, val):
        self.get_textbox(textbox).configure(state="normal")
        self.get_textbox(textbox).insert(tk.END, val + "\n")
        self.get_textbox(textbox).configure(state="disabled")

    ################
    # --> EVENTS <--
    ################

    def e_remove_order(self):
        self.orders_database.cursor.execute("UPDATE tables SET table_status = 0 WHERE table_id = (SELECT table_id FROM orders WHERE order_id = ?)", (self.var_order_id_entry.get(),))
        self.orders_database.remove_order(self.var_order_id_entry.get())
        self.orders_database.conn.commit()
        self.refresh_orders()


def run():
    root = tk.Tk()
    app = RestaurantGuiApp(root)
    app.run()