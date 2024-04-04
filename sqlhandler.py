import sqlite3

class RestaurantDatabase:
    def __init__(self):
        self.conn = sqlite3.connect("Restaurant.db")
        self.cursor = self.conn.cursor()
        self.init()

    def init(self):
        self.set_foreign_key(True)
        self.create_tables()
        self.insert_tables_if_empty()

    def execute_sql_query(self, cmd, params=None):
        if params:
            self.cursor.execute(cmd, params)
        else:
            self.cursor.execute(cmd)
        self.conn.commit()
        return self.cursor.fetchall()

    def create_tables(self):
        self.execute_sql_query("CREATE TABLE IF NOT EXISTS orders (order_id INTEGER PRIMARY KEY, customer_name TEXT, order_type TEXT, full_order TEXT, address TEXT, table_id INTEGER, total INTEGER, FOREIGN KEY (table_id) REFERENCES tables(table_id))")
        self.execute_sql_query("CREATE TABLE IF NOT EXISTS tables (table_id INTEGER PRIMARY KEY, table_status INTEGER)")

    def insert_tables_if_empty(self):
        if self.get_table_count() == 0:
            for _ in range(50):
                self.execute_sql_query("INSERT INTO tables (table_status) VALUES (?)", (0,))

    def get_table_count(self):
        res = self.execute_sql_query("SELECT COUNT(*) FROM tables")[0]
        return int(str(res).strip("(,)"))
        
    def set_foreign_key(self, state):
        self.execute_sql_query("PRAGMA foreign_keys = ON" if state else "PRAGMA foreign_keys = on")
    
    def add_order(self, customer_name : str, order_type : str, order : list, address : str, table : int, total : int):
        self.execute_sql_query("INSERT INTO orders (customer_name, order_type, full_order, address, table_id, total) VALUES (?, ?, ?, ?, ?, ?)", (customer_name, order_type, ' '.join(order), address, table, total))
        
    def remove_order(self, order_id : int):
        self.execute_sql_query("DELETE FROM orders WHERE order_id == ?", (order_id,))

    def return_all_orders(self):
        return self.execute_sql_query("SELECT * FROM orders")
    
    def get_next_free_table(self):
        res = self.execute_sql_query("SELECT table_id FROM tables WHERE table_status = 0 LIMIT 1")
        return int(str(res[0]).strip("(,)"))
        
    def set_table_status(self, table_id : int, table_status : int):
        self.execute_sql_query("UPDATE tables SET table_status = ? WHERE table_id = ?", (table_status, table_id))