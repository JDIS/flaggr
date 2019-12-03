"""Event marshmallow schemas"""
from flask_rebar import RequestSchema
from marshmallow import fields, Schema

class AdminEventRequestSchema(RequestSchema):
    """Response schema for getting a flag"""
    name = fields.String(required=True)
    teams = fields.Boolean(required=True)
    is_open = fields.Boolean(required=True)
    is_visible = fields.Boolean(required=True)
    url = fields.String()
    front_page = fields.String()
    flag_format = fields.String()

    # À voir si on veut les retourner là ou dans un call à part)*
    #admins = fields.nested(AdminSchema, required=True)

class AdminEventListSchema(Schema):
    """Response schema for getting a flag"""
    id = fields.Integer(required=True)
    name = fields.String(required=True)
    is_open = fields.Boolean(required=True)
    is_visible = fields.Boolean(required=True)

class AdminEventSchema(Schema):
    """Response schema for getting a flag"""
    name = fields.String(required=True)
    url = fields.String(required=True)
    flag_format = fields.String(required=True)
    is_open = fields.Boolean(required=True)
    is_visible = fields.Boolean(required=True)

    # À voir si on veut les retourner là ou dans un call à part)*
    #admins = fields.nested(AdminSchema, required=True)