"""Category marshmallow schemas"""

from marshmallow import fields, Schema


class CategorySchema(Schema):
    """Response schema for getting a category"""
    id = fields.Integer(required=True)
    event_id = fields.Integer(required=True)
    name = fields.String(required=True)

