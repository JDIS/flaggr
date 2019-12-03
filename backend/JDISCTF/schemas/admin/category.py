"""Challenge marshmallow schemas"""
from flask_rebar import RequestSchema
from marshmallow import fields, Schema

from JDISCTF.schemas.admin.flag import FlagSchema
from JDISCTF.schemas.category import CategorySchema

class AdminCategoryRequestSchema(RequestSchema):
    """Request schema for creating a category"""

    name = fields.String(required=True)
    event_id = fields.Integer(required=True)

class AdminCategorySchema(Schema):
    """Response schema for getting a category"""
    id = fields.Integer(required=True)
    name = fields.String(required=True)
    event_id = fields.Integer(required=True)
