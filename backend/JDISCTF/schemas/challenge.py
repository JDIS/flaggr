"""Challenge marshmallow schemas"""
from flask_rebar import RequestSchema
from marshmallow import fields, Schema

from JDISCTF.schemas.category import CategorySchema
from JDISCTF.schemas.submission import TeamSubmissionSchema


class UserChallengeSchema(Schema):
    """Response schema for getting a challenge"""
    id = fields.Integer(required=True)
    category_id = fields.Integer(required=True)
    name = fields.String(required=True)
    description = fields.String(required=True)
    points = fields.Integer(required=True)
    solves = fields.Nested(TeamSubmissionSchema, required=True, many=True)
    is_solved = fields.Boolean()


class ChallengeByCategorySchema(CategorySchema):
    """Response schema for getting challenges grouped by category"""
    challenges = fields.Nested(UserChallengeSchema, many=True)


class SubmitFlagSchema(RequestSchema):
    """Schema for submitting a flag for a given challenge"""
    flag = fields.String(required=True)


class SubmitFlagResponseSchema(Schema):
    """Schema for the response of a flag submission"""
    correct = fields.Boolean(required=True)
