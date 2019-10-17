"""Challenge marshmallow schemas"""

from marshmallow import fields, Schema
from JDISCTF.schemas import CategorySchema


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
