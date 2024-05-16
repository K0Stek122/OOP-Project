import sqlite3

class RestaurantDatabase:
    
    #########################################
    #CONSTRUCTORS AND QUALITY OF LIFE FUNCS #
    #########################################
    
    def __init__(self):
        self.conn = sqlite3.connect("Restaurant.db")
        self.cursor = self.conn.cursor()
        self.initialise_restaurant()

    def initialise_restaurant(self):
        self.set_foreign_key(True)
        self.create_tables_relation()
        self.insert_tables_if_empty()

    def execute_sql_query(self, cmd, params=None):
        """Executes arbitrary SQL Queries

        Args:
            cmd (string): The SQL Command to be execeuted

        Returns:
            cursor.fetchall(): The output of the SQL Query, if the output was a Data Query Language query
        """        
        if params:
            self.cursor.execute(cmd, params)
        else:
            self.cursor.execute(cmd)
        self.conn.commit()
        return self.cursor.fetchall()

    def create_tables_relation(self):     
        self.execute_sql_query("CREATE TABLE IF NOT EXISTS orders (order_id INTEGER PRIMARY KEY, customer_name TEXT, order_type TEXT, full_order TEXT, address TEXT, table_id INTEGER, total INTEGER, FOREIGN KEY (table_id) REFERENCES tables(table_id))")
        self.execute_sql_query("CREATE TABLE IF NOT EXISTS tables (table_id INTEGER PRIMARY KEY, table_status INTEGER)")

    def insert_tables_if_empty(self):
        if self.get_table_count() == 0:
            for _ in range(50):
                self.execute_sql_query("INSERT INTO tables (table_status) VALUES (?)", (0,))
    
    def add_order(self, customer_name : str, order_type : str, order : list, address : str, table : int, total : int):
        """Inserts a new order into the order relation

        Args:
            customer_name (str): The name of the customer
            order_type (str): Order type: Takeaway, Dine In, Delivery
            order (list): List of the items that are ordered
            address (str): Address if the order is a Delivery Order, otherwise left null
            table (int): Unique ID of the table
            total (int): The amount that needs to be paid by the customer.
        """        
        self.execute_sql_query("INSERT INTO orders (customer_name, order_type, full_order, address, table_id, total) VALUES (?, ?, ?, ?, ?, ?)", (customer_name, order_type, ' '.join(order), address, table, total,))
        
    def remove_order(self, order_id : int):
        self.execute_sql_query("DELETE FROM orders WHERE order_id == ?", (order_id,))

    def return_all_orders(self):
        return self.execute_sql_query("SELECT * FROM orders")
    
    #######################
    # GETTERS AND SETTERS #
    #######################
    
    def get_table_count(self):
        res = self.execute_sql_query("SELECT COUNT(*) FROM tables")[0]
        return int(str(res).strip("(,)")) #This line will prettify the query output
        
    def set_foreign_key(self, state):
        self.execute_sql_query("PRAGMA foreign_keys = ON" if state else "PRAGMA foreign_keys = on")
    
    def get_next_free_table(self):
        res = self.execute_sql_query("SELECT table_id FROM tables WHERE table_status = 0 LIMIT 1")
        return int(str(res[0]).strip("(,)"))
        
    def set_table_status(self, table_id : int, table_status : int):
        self.execute_sql_query("UPDATE tables SET table_status = ? WHERE table_id = ?", (table_status, table_id))