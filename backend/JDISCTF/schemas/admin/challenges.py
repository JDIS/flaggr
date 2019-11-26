"""Challenge marshmallow schemas"""
from flask_rebar import RequestSchema
from marshmallow import fields, Schema

from JDISCTF.schemas.category import CategorySchema


class AdminChallengeListSchema(Schema):
    id = fields.Integer(required=True)
    name = fields.String(required=True)
    category = fields.Nested(CategorySchema, only="name", required=True)
    hidden = fields.Boolean(required=True)
    