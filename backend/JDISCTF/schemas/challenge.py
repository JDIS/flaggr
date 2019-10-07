"""Challenge marshmallow schemas"""

from marshmallow import fields, Schema


class ChallengeSchema(Schema):
    """Response schema for getting a challenge"""
    id = fields.Integer(required=True)
    category_id = fields.Integer(required=True)
    name = fields.String(required=True)
    description = fields.String(required=True)
    points = fields.Integer(required=True)
