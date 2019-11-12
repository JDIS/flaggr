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

class TeamRequestSchema(Schema):
    """Schema that represents a team request"""
    user = fields.Nested(UserSchema)
    name = fields.String(required=True)


class CreateTeamRequestSchema(RequestSchema):
    """Schema to create a team"""
    name = fields.String(required=True)


class JoinTeamRequestSchema(RequestSchema):
    """Schema to request to join a team"""
    team_id = fields.Integer(required=True)


class SendTeamRequestRequestSchema(RequestSchema):
    team_id = fields.Integer(required=True)


class SendTeamRequestSchema(RequestSchema):
    pass


class AcceptTeamRequestRequestSchema(Schema):
    user_id = fields.Integer(required=True)


class AcceptTeamRequestSchema(Schema):
    pass


class DeclineTeamRequestRequestSchema(RequestSchema):
    user_id = fields.Integer(required=True)


class DeclineTeamRequestSchema(Schema):
    pass


class KickTeamMemberRequestSchema(RequestSchema):
    user_id = fields.Integer(required=True)


class KickTeamMemberSchema(Schema):
    pass


class ChangeRoleRequestSchema(RequestSchema):
    user_id = fields.Integer(required=True)


class ChangeRoleSchema(Schema):
    pass


class DeleteTeamRequestRequestSchema(RequestSchema):
    pass


class DeleteTeamRequestSchema(Schema):
    pass
