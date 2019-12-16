"""Challenge marshmallow schemas"""
from flask_rebar import RequestSchema
from marshmallow import fields, Schema

from JDISCTF.schemas.admin.category import AdminCategorySchema
from JDISCTF.schemas.admin.flag import FlagSchema


class AdminChallengeRequestSchema(RequestSchema):
    """Request schema for creating a challenge"""
    category_id = fields.Integer(required=True)

    name = fields.String(required=True)
    description = fields.String(required=True)
    points = fields.Integer(required=True)
    flags = fields.Nested(FlagSchema, required=True, many=True)

    hidden = fields.Boolean(required=True)


class AdminChallengeListSchema(Schema):
    """Response schema for challenge listing"""

    id = fields.Integer(required=True)
    name = fields.String(required=True)
    category = fields.Nested(AdminCategorySchema, only="name", required=True)
    hidden = fields.Boolean(required=True)
    points = fields.Integer(required=True)


class AdminChallengeSchema(Schema):
    """Response schema for getting a challenge"""

    id = fields.Integer(required=True)
    category = fields.Nested(AdminCategorySchema)
    flags = fields.Nested(FlagSchema, many=True)

    name = fields.String(required=True)
    description = fields.String(required=True)
    points = fields.Integer(required=True)

    is_solved = fields.Boolean()
    hidden = fields.Boolean(required=True)
