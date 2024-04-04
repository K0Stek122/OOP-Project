import sqlite3

class RestaurantDatabase:
    def __init__(self):
        self.conn = sqlite3.connect("Restaurant.db")
        self.cursor = self.conn.cursor()
        self.create_tables()

    def create_tables(self):
        self.set_foreign_keys()
        
        self.cursor.execute("CREATE TABLE IF NOT EXISTS orders (order_id INTEGER PRIMARY KEY, customer_name TEXT, order_type TEXT, full_order TEXT, address TEXT, table_id INTEGER, total INTEGER, FOREIGN KEY (table_id) REFERENCES tables(table_id))")
        self.conn.commit()
        self.cursor.execute("CREATE TABLE IF NOT EXISTS tables (table_id INTEGER PRIMARY KEY, table_status INTEGER)")
        self.conn.commit()
        
        self.initialise_tables()

    def initialise_tables(self):
        self.cursor.execute("SELECT COUNT(*) FROM tables")
        res = self.cursor.fetchall()
        if res[0] == 0:
            self.set_tables()
        self.set_tables(50)
        
    def set_foreign_keys(self, state = True):
            self.cursor.execute("PRAGMA foreign_keys = ON" if state else "PRAGMA foreign_keys = on")
            self.conn.commit()

    def set_tables(self, amnt : int):
        for i in range(amnt):
            self.cursor.execute("INSERT INTO tables (table_status) VALUES (?)", (0,))
            self.conn.commit()
    
    def add_order(self, customer_name : str, order_type : str, order : list, address : str, table : int, total : int):
        self.cursor.execute("INSERT INTO orders (customer_name, order_type, full_order, address, table_id, total) VALUES (?, ?, ?, ?, ?, ?)", (customer_name, order_type, ' '.join(order), address, table, total))
        self.conn.commit()
        
    def remove_order(self, order_id : int):
        self.cursor.execute("DELETE FROM orders WHERE order_id == ?", (order_id,))
        self.conn.commit()

    def return_all_orders(self):
        self.cursor.execute("SELECT * FROM orders")
        return self.cursor.fetchall()
    
    def get_next_free_table(self):
        self.cursor.execute("SELECT table_id FROM tables WHERE table_status = 0 LIMIT 1")
        return int(str(self.cursor.fetchall()[0]).strip("(,)"))
        
    def set_table_status(self, table_id : int, table_status : int):
        self.cursor.execute("UPDATE tables SET table_status = ? WHERE table_id = ?", (table_status, table_id))
        self.conn.commit()