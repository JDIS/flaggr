"""Event marshmallow schemas"""
from flask_rebar import RequestSchema
from marshmallow import fields, Schema

class AdminEventRequestSchema(RequestSchema):
    """Response schema for getting an event"""
    name = fields.String(required=True)
    teams = fields.Boolean(required=True)
    is_open = fields.Boolean(required=True)
    is_visible = fields.Boolean(required=True)
    url = fields.String()
    front_page = fields.String()
    flag_format = fields.String()


class AdminEventListSchema(Schema):
    """Response schema for getting an event"""
    id = fields.Integer(required=True)
    name = fields.String(required=True)
    is_open = fields.Boolean(required=True)
    is_visible = fields.Boolean(required=True)


class AdminEventSchema(Schema):
    """Response schema for getting an event"""
    name = fields.String(required=True)
    # url = fields.String(required=True)
    flag_format = fields.String(required=True)
    is_open = fields.Boolean(required=True)
    is_visible = fields.Boolean(required=True)
    front_page = fields.String(required=True)
    teams = fields.Boolean(required=True)
