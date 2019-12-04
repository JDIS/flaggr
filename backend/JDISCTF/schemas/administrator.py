"""Administrators marshmallow schemas"""

from flask_rebar import ResponseSchema
from marshmallow import fields

from JDISCTF.schemas.user import UserSchema


class AdministratorSchema(ResponseSchema):
    """Response schema for getting an admin"""
    id = fields.Integer()
    is_platform_admin = fields.Boolean()
    user = fields.Nested(UserSchema)
