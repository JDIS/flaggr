"""Authentication routes"""

import flask_rebar
from flask_rebar import errors
from flask_login import current_user, login_user, logout_user
from JDISCTF.app import DB, REGISTRY
from JDISCTF.models import User, Participant
from JDISCTF.schemas import CreateUserSchema, GenericMessageSchema, LoginSchema, UserSchema, ParticipantSchema


@REGISTRY.handles(
    rule="/login",
    method="POST",
    request_body_schema=LoginSchema(),
    response_body_schema={200: UserSchema()},
)
def login():
    """Login a user"""
    if current_user.is_authenticated:
        return current_user

    body = flask_rebar.get_validated_body()
    email = body["email"]
    password = body["password"]
    remember = body["remember"]

    user = User.query.filter_by(email=email).first()
    if user is None or not user.check_password(password):
        raise errors.UnprocessableEntity("Invalid email or password.")

    login_user(user, remember=remember)

    return user


@REGISTRY.handles(
    rule="/logout",
    method="GET",
    response_body_schema={200: GenericMessageSchema()},
)
def logout():
    """Logouts the user"""
    logout_user()
    return "OK"


@REGISTRY.handles(
    rule="/register",
    method="POST",
    request_body_schema=CreateUserSchema(),
    response_body_schema={201: ParticipantSchema()},
)
def register_participant():
    """Register a new user"""
    body = flask_rebar.get_validated_body()
    email = body["email"]
    username = body["username"]
    password = body["password"]

    # FIXME: event_id should be sourced from the link.
    event_id = 0

    # Validate user uniqueness constraint.
    user = User.query.filter_by(email=email).first()

    if user is not None and user.participant and user.participant.event_id == event_id:
        raise errors.UnprocessableEntity("A participant with that email already exists for this event")

    user = User.query.filter_by(username=username).first()

    if user is not None and user.participant and user.participant.event_id == event_id:
        raise errors.UnprocessableEntity("A participant with that username already exists for this event")
    user = User(email=email, username=username)
    user.set_password(password)

    DB.session.add(user)
    DB.session.commit()
    
    participant = Participant(event_id=event_id, user_id=user.id)
    DB.session.add(participant)
    DB.session.commit()

    return user, 201
