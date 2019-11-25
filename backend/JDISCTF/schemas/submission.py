"""Submission marshmallow schemas"""
from marshmallow import fields, Schema

from JDISCTF.schemas.team import TeamBasicInfoSchema


class OwnTeamSubmissionSchema(Schema):
    """
    Schema for a submission for your own team
    (meaning that its okay to see successful and failed flags)
    """
    input = fields.String(required=True)
    is_correct = fields.Boolean(required=True)
    time = fields.DateTime(required=True)


class TeamSubmissionSchema(Schema):
    """
    Schema for a submission for a rival team
    (meaning that its NOT okay to see successful and failed flags)
    """
    is_correct = fields.Boolean(required=True)
    time = fields.DateTime(required=True)
    team = fields.Nested(TeamBasicInfoSchema, required=True)
