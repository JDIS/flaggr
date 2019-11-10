"""Team marshmallow schemas"""

from flask_rebar import RequestSchema
from marshmallow import fields, Schema
from JDISCTF.schemas.user import UserSchema


class TeamMemberSchema(Schema):
    """Schema for getting a team member's information"""
    user = fields.Nested(UserSchema)
    captain = fields.Bool()
    

class JoinRequestSchema(Schema):
    """Schema for getting a user's request to join a team"""
    user = fields.Nested(UserSchema)
    requested_at = fields.DateTime()


class TeamSchema(Schema):
    """Response schema for getting a team's information"""
    id = fields.Integer(required=True)
    event_id = fields.Integer(required=True)
    name = fields.String(required=True)

    members = fields.Nested(TeamMemberSchema, many=True)
    requests = fields.Nested(JoinRequestSchema, many=True)

class JoinTeamRequest(Schema):
    """Response schema for requesting to join a team"""
    message = fields.String()


class CreateTeamSchema(RequestSchema):
    """Schema to create a team"""
    name = fields.String(required=True)


class JoinTeamRequestSchema(RequestSchema):
    """Schema to request to join a team"""
    team_id = fields.Integer(required=True)

    