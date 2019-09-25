import flask_rebar
from flask_rebar import errors
from JDISCTF import db, registry
from JDISCTF.models import User
from JDISCTF.schemas import createUserSchema, userSchema

@registry.handles(
    rule="/users/<int:user_id>",
    method="GET",
    response_body_schema=userSchema
)
def get_user(user_id: int):
    user = User.query.filter_by(id=user_id).first()

    if user is None:
        raise errors.NotFound()

    return user
