"""Authentication routes for administration"""

import flask_rebar
from flask_login import login_user
from flask_rebar import errors

from JDISCTF.app import DB, REGISTRY
from JDISCTF.models import Administrator, User
from JDISCTF.schemas import AdministratorSchema, CreateUserSchema, LoginSchema


@REGISTRY.handles(
    rule="/admin/login",
    method="POST",
    request_body_schema=LoginSchema(),
    response_body_schema={200: AdministratorSchema()},
    authenticators=None
)
def login_administrator():
    """Login an administrator"""

    body = flask_rebar.get_validated_body()
    email = body["email"]
    password = body["password"]
    remember = body["remember"] if "remember" in body else False

    user = User.query.filter_by(email=email).first()
    if user is None or not user.check_password(password):
        raise errors.UnprocessableEntity("Invalid email or password.")

    administrator = user.get_administrator()
    if administrator is None:
        raise errors.Unauthorized("You must be an administrator to access this resource.")

    login_user(user, remember=remember)

    return administrator


@REGISTRY.handles(
    rule="/admin/register",
    method="POST",
    request_body_schema=CreateUserSchema(),
    response_body_schema={201: AdministratorSchema()},
    authenticators=None
)
def register_administrator():
    """Register a new user"""
    body = flask_rebar.get_validated_body()
    email = body["email"]
    username = body["username"]
    password = body["password"]

    # Validate user uniqueness constraint.
    user = User.query.filter_by(email=email).first()
    if user is not None:
        administrator = user.get_administrator()

        if administrator is not None:
            raise errors.UnprocessableEntity("An administrator with that email already exists")

    user = User.query.filter_by(username=username).first()
    if user is not None:
        administrator = user.get_administrator()

        if administrator:
            raise errors.UnprocessableEntity("An administrator with that username already exists for this event")

    user = User(email=email, username=username)
    user.set_password(password)

    administrator = Administrator(is_platform_admin=False, user=user)

    DB.session.add(administrator)
    DB.session.commit()

    return administrator, 201
