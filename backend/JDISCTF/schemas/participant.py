from marshmallow import Schema, fields

from JDISCTF.schemas import UserSchema


class ParticipantSchema(Schema):
    """Schema for getting a participants's info"""
    id = fields.Integer()
    user = fields.Nested(UserSchema)
