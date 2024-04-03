import tkinter as tk

import backend
import frontend

if __name__ == "__main__":
    root = tk.Tk()
    frontend.CreateOrderGui(root).pack(side="top", fill="both", expand=True)
    print("Hello World")
    root.mainloop()