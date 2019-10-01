"""Users schemas"""

from marshmallow import fields, Schema
from flask_rebar import RequestSchema


class CreateUserSchema(RequestSchema):
    """Schema for creating a new user"""
    email = fields.String(required=True)
    username = fields.String(required=True)
    password = fields.String(required=True)


class UserSchema(Schema):
    """Schema for getting a user's info"""
    class Meta:
        """Schema fields"""
        # Fields to expose
        fields = ("email", "username")


USER_SCHEMA = UserSchema()
CREATE_USER_SCHEMA = CreateUserSchema()
