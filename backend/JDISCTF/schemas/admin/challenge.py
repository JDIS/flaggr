"""Challenge marshmallow schemas"""
from flask_rebar import RequestSchema
from marshmallow import fields, Schema

from JDISCTF.schemas.admin.flag import FlagSchema
from JDISCTF.schemas.category import CategorySchema


class AdminChallengeRequestSchema(RequestSchema):
    category_id = fields.Integer(required=True)

    name = fields.String(required=True)
    description = fields.String(required=True)
    points = fields.Integer(required=True)

    hidden = fields.Boolean(required=True)

class AdminChallengeListSchema(Schema):
    id = fields.Integer(required=True)
    name = fields.String(required=True)
    category = fields.Nested(CategorySchema, only="name", required=True)
    hidden = fields.Boolean(required=True)
    

class AdminChallengeSchema(Schema):
    id = fields.Integer(required=True)
    category_id = fields.Integer(required=True)
    
    name = fields.String(required=True)
    description = fields.String(required=True)
    points = fields.Integer(required=True)

    is_solved = fields.Boolean()
    hidden = fields.Boolean(required=True)


class AdminChallengeInformationSchema(Schema):
    """Response schema for getting a challenge"""
    challenge = fields.Nested(AdminChallengeSchema, required=True)
    flags = fields.Nested(FlagSchema, many=True)

    # En ordre de priorité
    #FIXMEMAX : files = nested
    #FIXMEMAX : links = nested
    #FIXMEMAX : tags = nested