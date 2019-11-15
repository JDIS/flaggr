"""Team marshmallow schemas"""

from flask_rebar import RequestSchema
from marshmallow import fields, Schema

from JDISCTF.schemas.user import UserSchema


class TeamMemberSchema(Schema):
    """Schema for getting a team member's information"""
    user = fields.Nested(UserSchema)
    captain = fields.Bool()

# TODO : Voir avec émilio / sarah si une route doit exposer cette information là
class JoinRequestSchema(Schema):
    """Schema for getting a user's request to join a team"""
    user = fields.Nested(UserSchema)
    requested_at = fields.DateTime()


class TeamSchema(Schema):
    """Schema for getting a team's information"""
    id = fields.Integer(required=True)
    event_id = fields.Integer(required=True)
    name = fields.String(required=True)

    members = fields.Nested(TeamMemberSchema, many=True)
    requests = fields.Nested(JoinRequestSchema, many=True)

class TeamRequestSchema(Schema):
    """Schema that represents a team request"""
    user = fields.Nested(UserSchema)
    team = fields.Nested(TeamSchema)


class CreateTeamRequestSchema(RequestSchema):
    """Request schema to create a team request"""
    name = fields.String(required=True)


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
