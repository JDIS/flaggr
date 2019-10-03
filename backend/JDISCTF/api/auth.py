"""Authentication routes"""

import flask_rebar
from flask_rebar import errors
from JDISCTF.app import DB, REGISTRY
from JDISCTF.models import User
from JDISCTF.schemas import USER_SCHEMA, CREATE_USER_SCHEMA


@REGISTRY.handles(
    rule="/register",
    method="POST",
    request_body_schema=CREATE_USER_SCHEMA,
    response_body_schema={201: USER_SCHEMA},
)
def register():
    """Register a new user"""
    body = flask_rebar.get_validated_body()
    email = body["email"]
    username = body["username"]
    password = body["password"]

    # Validate user uniqueness constraint.
    user = User.query.filter_by(email=email).first()

    if user is not None:
        raise errors.Conflict("A user with that email already exists")

    user = User.query.filter_by(username=username).first()

    if user is not None:
        raise errors.Conflict("A user with that username already exists")

    user = User(email=email, username=username)
    user.set_password(password)

    DB.session.add(user)
    DB.session.commit()

    return user, 201
