"""Challenges routes"""
import re

import flask_rebar
from flask_login import current_user
from flask_rebar import errors
from sqlalchemy.orm import contains_eager

from JDISCTF.app import DB, REGISTRY
from JDISCTF.flask_login_authenticator import FlaskLoginAuthenticator
from JDISCTF.models import Category, Challenge, Event, Flag, Submission
from JDISCTF.schemas import ChallengeByCategorySchema, GenericMessageSchema,\
    SubmitFlagResponseSchema, SubmitFlagSchema, UserChallengeSchema

from JDISCTF.schemas.admin import AdminChallengeInformationSchema, AdminChallengeListSchema, AdminChallengeRequestSchema


@REGISTRY.handles(
    rule="/admin/challenges/event/<int:event_id>",
    method="GET",
    response_body_schema=AdminChallengeListSchema(many=True)
    # Commented for dev
    # TOOD : Admin-only decorators
    #authenticators=FlaskLoginAuthenticator() 
)
def get_admin_challenges(event_id: int):
    """Get all the challenges for a given event"""
    event = Event.query.filter_by(id=event_id).first()

    if event is None:
        raise errors.NotFound(f'Event with id "{event_id}" not found.')

    challenges = Challenge.query.join(Category).filter_by(event_id=event_id).all()

    return challenges


@REGISTRY.handles(
    rule="/admin/challenges/<int:challenge_id>",
    method="GET",
    response_body_schema=AdminChallengeInformationSchema(),
    # Commented for dev
    # TOOD : Admin-only decorators
    #authenticators=FlaskLoginAuthenticator()
)
def get_admin_challenge(challenge_id: int):
    """Get a single challenge by its id"""
    challenge = Challenge.query.filter_by(id=challenge_id).first()
    flags = Flag.query.filter_by(challenge_id=challenge_id).all()
    # TODO : Add tags
    # TODO : Add files
    # TODO : Add links

    if challenge is None:
        raise errors.NotFound(f'Challenge with id "{challenge_id}" not found.')

    # FIXME Missing validations. If the current admin is admin of challenge.category.event_id

    return {"challenge": challenge, "flags": flags}


@REGISTRY.handles(
    rule="/admin/challenges",
    method="POST",
    request_body_schema=AdminChallengeRequestSchema(),
    response_body_schema=AdminChallengeInformationSchema(),
    # Commented for dev
    # TOOD : Admin-only decorators
    #authenticators=FlaskLoginAuthenticator()
)
def create_challenge():
    """Add a challenge and its associated ressources (flags, links, files)"""
    body = flask_rebar.get_validated_body()
    name = body["name"]
    points = body["points"]
    hidden = body["hidden"]
    description = body["description"]
    category_id = body["category_id"]

    if not name:
        raise errors.UnprocessableEntity("Name must not be empty.")

    if points < 0:
        raise errors.UnprocessableEntity("Points must be positive.")

    challenge = Challenge.query.filter_by(name=name).first()

    if challenge is not None:
        raise errors.UnprocessableEntity("A challenge with that name already exists.")

    category = Category.query.filter_by(id=category_id).first()

    if category is None:
        raise errors.UnprocessableEntity("The category doesn't exist.")

    # FIXME Missing validations. If the current admin is admin of challenge.category.event_id

    challenge = Challenge(name=name, points=points, hidden=hidden, description=description, category_id=category_id)

    DB.session.add(challenge)
    DB.session.commit()

    return {"challenge": challenge}


@REGISTRY.handles(
    rule="/admin/challenges/<int:challenge_id>",
    method="PUT",
    request_body_schema=AdminChallengeRequestSchema(),
    response_body_schema=AdminChallengeInformationSchema(),
    # Commented for dev
    # TOOD : Admin-only decorators
    #authenticators=FlaskLoginAuthenticator()
)
def edit_challenge(challenge_id: int):
    """Add a challenge and its associated ressources (flags, links, files)"""
    body = flask_rebar.get_validated_body()
    name = body["name"]
    points = body["points"]
    hidden = body["hidden"]
    description = body["description"]
    category_id = body["category_id"]

    # FIXME Missing validations. If the current admin is admin of challenge.category.event_id

    editable_challenge = Challenge.query.filter_by(id=challenge_id).first()

    if editable_challenge is None:
        raise errors.UnprocessableEntity("This challenge does not exist.")

    if name != editable_challenge.name:
        if name is None:
            raise errors.UnprocessableEntity("Name must not be empty.")

        challenge = Challenge.query.filter_by(name=name).first()

        if challenge is not None:
            raise errors.UnprocessableEntity("A challenge with that name already exists.")


    if points != editable_challenge.points and points <= 0:
        raise errors.UnprocessableEntity("Points must be positive.")

    if category_id != editable_challenge.category_id:
        category = Category.query.filter_by(id=category_id).first()

        if category is None:
            raise errors.UnprocessableEntity("The category doesn't exist.")

    # FIXME Missing validations. If the current admin is admin of challenge.category.event_id

    editable_challenge.name = name
    editable_challenge.points = points
    editable_challenge.hidden = hidden
    editable_challenge.description = description
    editable_challenge.category_id = category_id

    print(editable_challenge)
    DB.session.commit()

    return {"challenge": editable_challenge}


@REGISTRY.handles(
    rule="/admin/challenges/<int:challenge_id>",
    method="DELETE",
    response_body_schema=GenericMessageSchema(),
    # Commented for dev
    # TOOD : Admin-only decorators
    #authenticators=FlaskLoginAuthenticator()
)
def delete_challenge(challenge_id: int):
    """Delete a challenge"""

    # TODO : should it delete it's associated ressources? (flags, links, files)
    # FIXME Missing validations. If the current admin is admin of challenge.category.event_id

    challenge = Challenge.query.filter_by(id=challenge_id).first()

    if challenge is None:
        raise errors.UnprocessableEntity("This challenge does not exist.")

    DB.session.delete(challenge)
    DB.session.commit()

    return ""