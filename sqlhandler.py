import sqlite3

class OrderDatabase:
    def __init__(self):
        self.conn = sqlite3.connect("Orders.db")
        self.cursor = self.conn.cursor()

        self.cursor.execute("CREATE TABLE IF NOT EXISTS orders (order_id INTEGER PRIMARY KEY, customer_name TEXT, order_type TEXT, full_order TEXT, address TEXT, table_num INTEGER, total INTEGER)")
        self.conn.commit()
    
    def add_order(self, customer_name : str, order_type : str, order : list, address : str, table : int, total : int):
        self.cursor.execute("INSERT INTO orders (customer_name, order_type, full_order, address, table_num, total) VALUES (?, ?, ?, ?, ?, ?)", (customer_name, order_type, ' '.join(order), address, table, total))
        self.conn.commit()

    def return_all_orders(self):
        self.cursor.execute("SELECT * FROM orders")
        return self.cursor.fetchall()
    
    def remove_order(self, order_id : int):
        self.cursor.execute("DELETE FROM orders WHERE order_id == ?", (order_id,))
        self.conn.commit()