#!/usr/bin/python3
import pathlib
import tkinter as tk
import pygubu
import re
import json

from tkinter import messagebox

PROJECT_PATH = pathlib.Path(__file__).parent
PROJECT_UI = PROJECT_PATH / "gui.ui"

class GuiApp:
    
    #--> INITIAL SETUP <--

    def __init__(self, master=None):
        self.builder = builder = pygubu.Builder()
        builder.add_resource_path(PROJECT_PATH)
        builder.add_from_file(PROJECT_UI)
        # Main widget
        self.mainwindow: ttk.Frame = builder.get_object("frame1", master)

        self.var_name_entry: tk.StringVar = None
        self.var_address_entry: tk.StringVar = None
        self.var_available_meals_combobox: tk.StringVar = None
        self.var_total_label: tk.StringVar = None
        builder.import_variables(self)

        builder.connect_callbacks(self)

    def run(self):
        # MEMBER VARIABLES
        self.final_order = []
        self.meal_price_index = {
            "Meal 1" : 5,
            "Meal 2" : 10,
            "Meal 3" : 15,
            "Meal 4" : 20,
            "Meal 5" : 25,
            "Meal 6" : 30,
        }

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

    def is_proper_name(self, name):
        if name == "" or not bool(re.match(r"^[A-Z][a-z]+\s[A-Z][a-z]+$", name)):
            return False
        return True
    
    def lock_entry(self, entry_name : str):
        self.get_entry(entry_name).configure(state="disabled")

    def append_to_textbox(self, textbox : str, val):
        self.get_textbox(textbox).configure(state="normal")
        self.get_textbox(textbox).insert(tk.END, val + "\n")
        self.get_textbox(textbox).configure(state="disabled")

    def lock_button(self, button : str):
        self.get_button(button).configure(state="disabled")

    def validate_name(self):
        if not self.is_proper_name(self.var_name_entry.get()):
            messagebox.showwarning("Improper name", "The name you have entered is improper.")
            return False
        name_entry : tk.Entry = self.builder.get_object("w_name_entry") #These two lines will lock the widget once the name is deemed to be proper.
        name_entry.configure(state="disabled")
        return True
    
    def lock_all_buttons(self):
        self.lock_button("w_dinein_button")
        self.lock_button("w_takeaway_button")
        self.lock_button("w_delivery_button")

    def calculate_total(self):
        return sum(self.meal_price_index[meal] for meal in self.final_order)

    def get_last_order(self):
        with open("../Orders.json", "r") as f:
            data = json.loads(f.read())
        if not data:
            return 1
        print(data)
        return int(data["Order ID"])

    ################
    # --> EVENTS <--
    ################

    def e_dinein(self):
        if not self.validate_name():
            return
        self.order_type = "Dine In"
        
        self.lock_entry("w_address_entry")
        self.lock_all_buttons()
        self.lock_all_buttons()
        self.lock_all_buttons()

    def e_takeaway(self):
        if not self.validate_name():
            return
        self.order_type = "Takeaway"
        self.lock_entry("w_address_entry")
        self.lock_all_buttons()
        self.lock_all_buttons()
        self.lock_all_buttons()

    def e_delivery(self):
        if not self.validate_name():
            return
        self.order_type = "Delivery"
        self.lock_all_buttons()
        self.lock_all_buttons()
        self.lock_all_buttons()

    def e_add_meal(self):
        self.final_order.append(self.var_available_meals_combobox.get())
        self.append_to_textbox("w_selected_meals_textbox", self.var_available_meals_combobox.get())

        self.var_total_label.set(f"Total: {self.calculate_total()}$")

    def e_order(self):
        if not self.var_name_entry.get():
            messagebox.showinfo("Empty Name", "Enter your name first.")
            return
        if len(self.final_order) <= 0:
            messagebox.showinfo("Empty order", "Cannot order nothing.")
            return
        if not self.var_address_entry.get() and self.order_type == "Delivery":
            messagebox.showinfo("Empty Address", "You have to input your address first.")
            return

        out = {
            "Order ID" : self.get_last_order() + 1,
            "Customer Name" : self.var_name_entry.get(),
            "Order Type" : self.order_type,
            "Order" : self.final_order,
            "Total" : self.calculate_total()
        }
        with open("./Orders.json", "a") as f:
            f.write(json.dumps(out, indent=4))
        messagebox.showinfo("Order Placed", "Your order has been placed, Thank You.")
        exit(0)

if __name__ == "__main__":
    root = tk.Tk()
    app = GuiApp(root)
    app.run()