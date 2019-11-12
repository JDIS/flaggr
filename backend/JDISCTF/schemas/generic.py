"""Generic marshmallow schemas"""

from marshmallow import fields, Schema


class GenericMessageSchema(Schema):
    """Response schema for getting a category"""
    name = fields.String(required=True)
