"""Team marshmallow schemas"""

from flask_rebar import RequestSchema
from marshmallow import fields, Schema
from JDISCTF.schemas.user import UserSchema


class TeamSchema(Schema):
    """Response schema for getting a team's information"""
    id = fields.Integer(required=True)
    event_id = fields.Integer(required=True)
    name = fields.String(required=True)

    members = fields.Nested(UserSchema, many=True)
    requests = fields.Nested(UserSchema, many=True)


class CreateTeamSchema(RequestSchema):
    """Response schema for getting a team's information"""
    name = fields.String(required=True)