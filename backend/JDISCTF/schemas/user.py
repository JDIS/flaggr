"""Users schemas"""

from marshmallow import fields, Schema
from flask_rebar import RequestSchema


class CreateUserSchema(RequestSchema):
    """Schema for creating a new user"""
    email = fields.Email(required=True)
    username = fields.String(required=True)
    password = fields.String(required=True)


class LoginSchema(RequestSchema):
    """Schema for logging-in a user"""
    email = fields.Email(required=True)
    password = fields.String(required=True)
    remember = fields.Boolean()


class LogoutSchema(Schema):
    """Schema for logging-out a user"""
    message = fields.String()


class UserSchema(Schema):
    """Schema for getting a user's info"""
    email = fields.Email()
    username = fields.String()
