"""Generic marshmallow schemas"""

from marshmallow import fields, Schema


class GenericMessageSchema(Schema):
    """Response schema for a message"""
    name = fields.String(required=True)
