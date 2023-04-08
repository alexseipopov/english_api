from marshmallow import Schema, fields


class UserSchema(Schema):
    id = fields.Integer()
    phone = fields.String()
    email = fields.String()
    password = fields.String()
