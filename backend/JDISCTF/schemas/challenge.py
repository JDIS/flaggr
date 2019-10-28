"""Challenge marshmallow schemas"""
from flask_rebar import RequestSchema
from marshmallow import fields, Schema
from JDISCTF.schemas.category import CategorySchema


class ChallengeSchema(Schema):
    """Response schema for getting a challenge"""
    id = fields.Integer(required=True)
    category_id = fields.Integer(required=True)
    name = fields.String(required=True)
    description = fields.String(required=True)
    points = fields.Integer(required=True)


class ChallengeByCategorySchema(CategorySchema):
    """Response schema for getting challenges grouped by category"""
    challenges = fields.Nested(ChallengeSchema, many=True)


class SubmitFlagSchema(RequestSchema):
    """Schema for submitting a flag for a given challenge"""
    team_id = fields.Integer(required=True)
    flag = fields.String(required=True)


class SubmitFlagResponseSchema(Schema):
    """Schema for the response of a flag submission"""
    correct = fields.Boolean(required=True)
