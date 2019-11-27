"""Challenge marshmallow schemas"""
from flask_rebar import RequestSchema
from marshmallow import fields, Schema

class FlagSchema(Schema):
    id = fields.Integer(required=True)
    challenge_id = fields.Integer(required=True)
    is_regex = fields.Boolean(required=True)
    value = fields.String(required=True)
