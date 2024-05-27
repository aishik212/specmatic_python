import itertools


class Product(object):
    id_iter = itertools.count(1)

    def __init__(self, name: str, type: str, inventory: int, id=0):
        self.name = name
        self.type = type
        self.inventory = inventory
        if id != 0:
            self.id = id
        else:
            self.id = next(Product.id_iter)


class Order(object):
    id_iter = itertools.count(1)

    def __init__(self, productid: int, count: int, status: str, id=0):
        self.productid = productid
        self.count = count
        self.status = status
        if id != 0:
            self.id = id
        else:
            self.id = next(Order.id_iter)


class Id(object):
    def __init__(self, id: int):
        self.id = id


