"""Team marshmallow schemas"""

from flask_rebar import RequestSchema
from marshmallow import fields, Schema

from JDISCTF.schemas.user import UserSchema


class TeamMemberSchema(Schema):
    """Schema for getting a team member's information"""
    user = fields.Nested(UserSchema)
    captain = fields.Bool()


class TeamRequestSchema(Schema):
    """Schema that represents a team request"""
    user = fields.Nested(UserSchema)
    team_name = fields.String(required=True)
    requested_at = fields.DateTime()


class TeamSchema(Schema):
    """Schema for getting a team's information"""
    id = fields.Integer(required=True)
    event_id = fields.Integer(required=True)
    team_name = fields.String(required=True)

    members = fields.Nested(TeamMemberSchema, many=True)
    requests = fields.Nested(TeamRequestSchema, many=True)


class CreateTeamRequestSchema(RequestSchema):
    """Request schema to create a team request"""
    team_name = fields.String(required=True)


class SendTeamRequestRequestSchema(RequestSchema):
    """Request schema to request to join a team"""
    team_id = fields.Integer(required=True)


class AcceptTeamRequestRequestSchema(RequestSchema):
    """Request schema when accepting a team request"""
    user_id = fields.Integer(required=True)


class DeclineTeamRequestRequestSchema(RequestSchema):
    """Request schema when declining a team request"""
    user_id = fields.Integer(required=True)


class KickTeamMemberRequestSchema(RequestSchema):
    """Request schema when kicking a team member"""
    user_id = fields.Integer(required=True)


class ChangeRoleRequestSchema(RequestSchema):
    """Request schema when changing a team member's role"""
    user_id = fields.Integer(required=True)
    captain = fields.Bool(required=True)
