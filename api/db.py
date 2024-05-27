from api.models import Product, Order


class Database:
    _products = {
        10: Product('XYZ Phone', 'gadget', 10, 10),
        20: Product('Gemini', 'dog', 10, 20)
    }

    _orders = {
        10: Order(10, 2, 'pending', 10),
        20: Order(10, 1, 'pending', 20)
    }

    @staticmethod
    def find_products(name: str, product_type: str, status: str):
        return [product for id, product in Database._products.items() if (
                product.name.lower() == name.lower()
                or product.type.lower() == product_type.lower()
                or Database.inventory_status(id) == status)]

    @staticmethod
    def find_product_by_id(product_id: int):
        return Database._products.get(product_id)

    @staticmethod
    def delete_product(product_id: int):
        if Database._products.get(product_id) is not None:
            del Database._products[product_id]

    @staticmethod
    def add_product(product: Product):
        Database._products[product.id] = product

    @staticmethod
    def update_product(product_id: int, product: Product):
        existing = Database.find_product_by_id(product_id)
        existing.name = product.name
        existing.type = product.type
        existing.inventory = product.inventory
        Database._products[product_id] = existing

    @staticmethod
    def inventory_status(product_id: int):
        product = Database.find_product_by_id(product_id)
        return 'sold' if product.inventory == 0 else 'available'

    @staticmethod
    def find_orders(product_id: int, status: str):
        return [order for id, order in Database._orders.items() if (
                order.productid == product_id
                or order.status.lower() == status.lower())]

    @staticmethod
    def find_order_by_id(order_id: int):
        return Database._orders.get(order_id)

    @staticmethod
    def delete_order(order_id: int):
        if Database._orders.get(order_id) is not None:
            del Database._orders[order_id]

    @staticmethod
    def add_order(order: Order):
        Database._orders[order.id] = order

    @staticmethod
    def reserve_product_inventory(product_id: int, count: int):
        product = Database._products.get(product_id)
        product.inventory -= count
        Database._products[product_id] = product

    @staticmethod
    def update_order(order: Order):
        existing = Database.find_order_by_id(order.id)
        existing.productid = order.productid
        existing.count = order.count
        existing.status = order.status
        Database._orders[order.id] = existing

