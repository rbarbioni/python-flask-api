from marshmallow import Schema, fields, INCLUDE


class AnySchema(Schema):
    class Meta:
        unknown = INCLUDE


class ProductSchema(Schema):
    id = fields.Integer()
    name = fields.String(required=True)
    code = fields.String(required=True)
    price = fields.Float(required=True)
    created_at = fields.Date(allow_none=True)
    updated_at = fields.Date(allow_none=True)


class UserSchema(Schema):
    id = fields.Integer()
    name = fields.String(required=True)
    email = fields.String(required=True)
    created_at = fields.Date(allow_none=True)
    updated_at = fields.Date(allow_none=True)
