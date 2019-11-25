"""Scoreboard marshmallow schemas"""
from flask_rebar import ResponseSchema
from marshmallow import fields


class ScoreboardSchema(ResponseSchema):
    """Response schema for the scoreboard"""
    team_name = fields.String(required=True)
    team_id = fields.Integer(required=True)
    points = fields.Number(required=True)
    position = fields.Integer(required=True)
    last_submission = fields.DateTime(required=True)
    solved_challenges = fields.Integer(required=True)
