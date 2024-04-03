import json

class Restaurant:
    def __init__(self, table_num, waiters):
        self.tables = [Table(i) for i in range(1, table_num + 1)]
        self.waiters = waiters
        self.orders = []
    def create_order(self, order_info: dict):
        if order_info["OrderType"] == "DineInOrder":
            self.orders.append(DineInOrder(order_info["CustomerName"], order_info["Order"], order_info["TableNumber"]))
        elif order_info["OrderType"] == "TakeawayOrder":
            self.orders.append(TakeawayOrder(order_info["CustomerName"], order_info["Order"]))
        else:
            self.orders.append(DeliveryOrder(order_info["CustomerName"], order_info["Order"], order_info["CustomerAddress"]))

class Table:
    def __init__(self, num, taken=False):
        self.num = num
        self.taken = taken

class Order:
    def __init__(self, customer_name, order):
        self.customer_name = customer_name
        self.order = order

class TakeawayOrder(Order):
    def __init__(self, customer_name, order):
        super().__init__(customer_name, order)

class DeliveryOrder(Order):
    def __init__(self, customer_name, order, address):
        super().__init__(customer_name, order)
        self.address = address

class DineInOrder(Order):
    def __init__(self, customer_name, order, table):
        super().__init__(customer_name, order)
        self.table = table

if __name__ == "__main__":
    pass