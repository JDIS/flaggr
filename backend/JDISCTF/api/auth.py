"""Authentication routes"""

import flask_rebar
from flask_login import login_user, logout_user
from flask_rebar import errors

from JDISCTF.app import DB, REGISTRY
from JDISCTF.models import Event, Participant, Team, TeamMember, User
from JDISCTF.permission_wrappers import require_event
from JDISCTF.schemas import CreateUserSchema, GenericMessageSchema, LoginSchema, ParticipantSchema


@REGISTRY.handles(
    rule="/event/<int:event_id>/login",
    method="POST",
    request_body_schema=LoginSchema(),
    response_body_schema={200: ParticipantSchema()},
    authenticators=None
)
@require_event
def login(event: Event):
    """Login a participant"""

    body = flask_rebar.get_validated_body()
    email = body["email"]
    password = body["password"]
    remember = body["remember"]

    participant = Participant.query\
        .join(Participant.user) \
        .filter(User.email == email,
                Participant.event_id == event.id)\
        .first()

    if participant is None or participant.user is None or not participant.user.check_password(password):
        raise errors.UnprocessableEntity("Invalid email or password.")

    login_user(participant.user, remember=remember)

    return participant


@REGISTRY.handles(
    rule="/logout",
    method="GET",
    response_body_schema={200: GenericMessageSchema()},
    authenticators=None
)
def logout():
    """Logouts the user"""
    logout_user()
    return "OK"


@REGISTRY.handles(
    rule="/event/<int:event_id>/register",
    method="POST",
    request_body_schema=CreateUserSchema(),
    response_body_schema={201: ParticipantSchema()},
    authenticators=None
)
@require_event
def register_participant(event: Event):
    """Register a new user"""
    body = flask_rebar.get_validated_body()
    email = body["email"]
    username = body["username"]
    password = body["password"]

    # Validate user uniqueness constraint.
    user = User.query.filter_by(email=email).first()
    if user is not None:
        participant = user.get_participant()

        if user is not None and participant and participant.event_id == event.id:
            raise errors.UnprocessableEntity("A participant with that email already exists for this event")

    user = User.query.filter_by(username=username).first()
    if user is not None:
        participant = user.get_participant()

        if user is not None and participant and participant.event_id == event.id:
            raise errors.UnprocessableEntity("A participant with that username already exists for this event")

    user = User(email=email, username=username)
    user.set_password(password)

    participant = Participant(event_id=event.id, user=user)

    DB.session.add(participant)

    if not event.teams:
        # means that its a solo event, need to create a team with the participant in it.
        team = Team(event_id=event.id, name=user.username,
                    members=[TeamMember(participant=participant, captain=True)])

        DB.session.add(team)

    DB.session.commit()

    login_user(participant.user, remember=True)

    return participant, 201
