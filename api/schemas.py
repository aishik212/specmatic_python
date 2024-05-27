from marshmallow import Schema, fields, post_load

from api.models import Product, Order


class ProductSchema(Schema):
    name = fields.Str()
    type = fields.Str()
    inventory = fields.Int()
    id = fields.Int(default=0)

    @post_load
    def make_product(self, data, **kwargs):
        return Product(**data)


class OrderSchema(Schema):
    productid = fields.Int()
    count = fields.Int()
    status = fields.Str()
    id = fields.Int(default=0)

    @post_load
    def make_order(self, data, **kwargs):
        return Order(**data)


class IdSchema(Schema):
    id = fields.Int()
