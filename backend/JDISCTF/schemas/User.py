from marshmallow import fields, Schema
from flask_rebar import RequestSchema

class CreateUserSchema(RequestSchema):
    email = fields.String(required=True)
    username = fields.String(required=True)
    password = fields.String(required=True)

class UserSchema(Schema):
    class Meta:
        # Fields to expose
        fields = ("email", "username")

userSchema = UserSchema()
createUserSchema = CreateUserSchema()