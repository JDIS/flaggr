"""Team marshmallow schemas"""

from flask_rebar import ResponseSchema
from marshmallow import fields


class EventSchema(ResponseSchema):
    """Schema for getting an event's information"""
    id = fields.Integer()
    name = fields.String()
    front_page = fields.String()
    teams = fields.Boolean()
