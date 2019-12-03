"""Challenge marshmallow schemas"""
from marshmallow import fields, Schema

class FlagSchema(Schema):
    """Response schema for getting a flag"""
    id = fields.Integer(required=True)
    challenge_id = fields.Integer(required=True)
    is_regex = fields.Boolean(required=True)
    value = fields.String(required=True)
