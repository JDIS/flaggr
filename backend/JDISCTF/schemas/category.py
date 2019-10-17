"""Category marshmallow schemas"""

from marshmallow import fields, schema


class CategorySchema(schema):
    id = fields.Integer(required=True)
    event_id = fields.Integer(required=True)
    name = fields.String(required=True)

