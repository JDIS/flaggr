"""Participant marshmallow schemas"""
from marshmallow import fields, Schema

from JDISCTF.schemas import UserSchema


class AdminParticipantListSchema(Schema):
    """Response schema for getting a list of participants"""
    id = fields.Integer(required=True)
    user = fields.Nested(UserSchema, required=True)
