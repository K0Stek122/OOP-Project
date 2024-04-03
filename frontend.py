import tkinter as tk
from tkinter import messagebox
import json
import re

import backend

class CreateOrderGui(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.restaurant = backend.Restaurant(50, 10)
        self.__setup_gui()

    def __setup_gui(self):
        self.parent.geometry("395x695")

        self.fullname_label = tk.Label(self, text="Full Name")
        self.fullname_label.grid(row=0, column=0, padx=10, pady=10)

        self.name_entry = tk.Entry(self)
        self.name_entry.grid(row=0, column=1, padx=10, pady=10)

        self.dine_in_button = tk.Button(self, text="Dine In", bg="lightgray", command=self.__e_DineInButton)
        self.dine_in_button.grid(row=1, column=0, padx=10, pady=10)

        self.takeaway_button = tk.Button(self, text="Takeaway", bg="lightgray", command=self.__e_TakeawayButton)
        self.takeaway_button.grid(row=1, column=1, padx=10, pady=10)

        self.delivery_button = tk.Button(self, text="Delivery", bg="lightgray", command=self.__e_DeliveryButton)
        self.delivery_button.grid(row=1, column=2, padx=10, pady=10)

        self.error_label = tk.Label(self, text="You need to enter a name first", fg="red")

    def __proper_name(self):
        if self.name_entry.get() == "" or not bool(re.match(r"^[A-Z][a-z]+\s[A-Z][a-z]+$", self.name_entry.get())):
            self.error_label.grid(row=2, column=1, padx=10, pady=10)
            return False
        self.error_label.destroy()
        return True

    def __e_DineInButton(self):
        if self.__proper_name():
            self.name_entry.config(state="readonly")

            self.order_label = tk.Label(self, text="Order")
            self.order_label.grid(row=3, column=0, padx=10, pady=10)

            self.order_listbox = tk.Listbox(self)
            self.order_listbox.grid(row=3, column=1, padx=10, pady=10)
            meals = ["Meal 1", "Meal 2", "Meal 3", "Meal 4", "Meal 5"]
            for meal in meals:
                self.order_listbox.insert(tk.END, meal)
            
            self.arrow_button = tk.Button(self, text="Add", bg="lightgray", command=self.__e_AddMeal)
            self.arrow_button.grid(row=4, column=1, padx=1, pady=10)
            self.selected_order_listbox = tk.Listbox(self)
            self.selected_order_listbox.grid(row=5, column=1, padx=10, pady=10)

            self.order_button = tk.Button(self, text="Order", bg="lightgray", command=lambda: self.__e_SaveOrder("DineInOrder"))
            self.order_button.grid(row=6, column=1, padx=10, pady=10)

    def __e_TakeawayButton(self):
        if self.__proper_name():
            self.order_flag = "DeliveryOrder"
            self.name_entry.config(state="readonly")

            self.order_label = tk.Label(self, text="Order")
            self.order_label.grid(row=3, column=0, padx=10, pady=10)

            self.order_listbox = tk.Listbox(self)
            self.order_listbox.grid(row=3, column=1, padx=10, pady=10)
            meals = ["Meal 1", "Meal 2", "Meal 3", "Meal 4", "Meal 5"]
            for meal in meals:
                self.order_listbox.insert(tk.END, meal)
            
            self.arrow_button = tk.Button(self, text="Add", bg="lightgray", command=self.__e_AddMeal)
            self.arrow_button.grid(row=4, column=1, padx=1, pady=10)
            self.selected_order_listbox = tk.Listbox(self)
            self.selected_order_listbox.grid(row=5, column=1, padx=10, pady=10)

            self.order_button = tk.Button(self, text="Order", bg="lightgray", command=lambda: self.__e_SaveOrder("TakeawayOrder"))
            self.order_button.grid(row=6, column=1, padx=10, pady=10)

    def __e_DeliveryButton(self):
        if self.__proper_name():
            self.order_flag = "DeliveryOrder"
            self.name_entry.config(state="readonly")

            self.addr_label = tk.Label(self, text="Address")
            self.addr_label.grid(row=2, column=0, padx=10, pady=10)

            self.addr_entry = tk.Entry(self)
            self.addr_entry.grid(row = 2, column=1, padx=10, pady=10)

            self.order_label = tk.Label(self, text="Order")
            self.order_label.grid(row=3, column=0, padx=10, pady=10)

            self.order_listbox = tk.Listbox(self)
            self.order_listbox.grid(row=3, column=1, padx=10, pady=10)
            meals = ["Meal 1", "Meal 2", "Meal 3", "Meal 4", "Meal 5"]
            for meal in meals:
                self.order_listbox.insert(tk.END, meal)
            
            self.arrow_button = tk.Button(self, text="Add", bg="lightgray", command=self.__e_AddMeal)
            self.arrow_button.grid(row=4, column=1, padx=1, pady=10)
            self.selected_order_listbox = tk.Listbox(self)
            self.selected_order_listbox.grid(row=5, column=1, padx=10, pady=10)

            self.order_button = tk.Button(self, text="Order", bg="lightgray", command=lambda: self.__e_SaveOrder("DeliveryOrder"))
            self.order_button.grid(row=6, column=1, padx=10, pady=10)

    def __e_AddMeal(self):
        if self.order_listbox.curselection() != None:
            self.selected_order_listbox.insert(tk.END, self.order_listbox.get(self.order_listbox.curselection()))

    def __e_SaveOrder(self, order_type):

        l_customer_address = lambda : "" if order_type != "DeliveryOrder" else self.addr_entry.get()
        l_table_number = lambda : -1 if order_type != "DineInOrder" else 0

        order_info = {
            "CustomerName" : self.name_entry.get(),
            "CustomerAddress" : l_customer_address(),
            "OrderType" : order_type,
            "Order" : self.selected_order_listbox.get(0, tk.END),
            "TableNumber" : l_table_number()
        }

        if order_type == "DineInOrder":
            messagebox.showinfo("Order", "Your order has been placed successfully! Your table is {TableNumber}")
        else:
            messagebox.showinfo("Order", "Your order has been placed successfully!")

        self.restaurant.create_order(order_info)
        self.parent.destroy()
