"""Challenges routes"""

import flask_rebar
from flask_rebar import errors

from JDISCTF.app import DB, REGISTRY
from JDISCTF.models import Administrator, Category, Challenge, Event, Flag, Submission
from JDISCTF.permission_wrappers import require_admin, require_admin_for_event
from JDISCTF.schemas import GenericMessageSchema

from JDISCTF.schemas.admin import AdminChallengeInformationSchema, AdminChallengeListSchema, AdminChallengeRequestSchema


@REGISTRY.handles(
    rule="/admin/challenges/event/<int:event_id>",
    response_body_schema=AdminChallengeListSchema(many=True)
)
@require_admin_for_event
def get_admin_challenges_for_event(_: Administrator, event_id: int):
    """Get all the challenges for a given event"""
    event = Event.query.filter_by(id=event_id).first()

    if event is None:
        raise errors.NotFound(f'Event with id "{event_id}" not found.')

    challenges = Challenge.query.join(Category).filter_by(event_id=event_id).all()

    return challenges


@REGISTRY.handles(
    rule="/admin/challenges/<int:challenge_id>",
    method="GET",
    response_body_schema=AdminChallengeInformationSchema()
)
@require_admin
def get_admin_challenge(current_admin: Administrator, challenge_id: int):
    """Get a single challenge by its id"""
    challenge = Challenge.query.filter_by(id=challenge_id).first()
    flags = Flag.query.filter_by(challenge_id=challenge_id).all()
    # TODOMAX : Add tags
    # TODOMAX : Add files
    # TODOMAX : Add links

    if challenge is None:
        raise errors.NotFound(f'Challenge with id "{challenge_id}" not found.')

    if not current_admin.is_admin_of_event(challenge.category.event_id):
        raise errors.Unauthorized("You do not have the permission to administer this challenge.")

    return {"challenge": challenge, "flags": flags}


@REGISTRY.handles(
    rule="/admin/challenges",
    method="POST",
    request_body_schema=AdminChallengeRequestSchema(),
    response_body_schema=AdminChallengeInformationSchema()
)
@require_admin
def create_challenge(current_admin: Administrator):
    """Add a challenge and its associated ressources (flags, links, files)"""
    body = flask_rebar.get_validated_body()
    name = body["name"]
    points = body["points"]
    hidden = body["hidden"]
    description = body["description"]
    category_id = body["category_id"]

    category = Category.query.filter_by(id=category_id).first()

    if category is None:
        raise errors.UnprocessableEntity("The category doesn't exist.")

    if not current_admin.is_admin_of_event(category.event_id):
        raise errors.Unauthorized("You do not have the permission to administer this challenge.")

    challenge = Challenge.query.filter_by(name=name).first()

    if challenge is not None:
        raise errors.UnprocessableEntity("A challenge with that name already exists.")

    if not name:
        raise errors.UnprocessableEntity("Name must not be empty.")

    if points <= 0:
        raise errors.UnprocessableEntity("Points must be positive.")

    challenge = Challenge(name=name, points=points, hidden=hidden, description=description, category_id=category_id)

    DB.session.add(challenge)
    DB.session.commit()

    return {"challenge": challenge}


@REGISTRY.handles(
    rule="/admin/challenges/<int:challenge_id>",
    method="PUT",
    request_body_schema=AdminChallengeRequestSchema(),
    response_body_schema=AdminChallengeInformationSchema()
)
@require_admin
def edit_challenge(current_admin: Administrator, challenge_id: int):
    """Edit a challenge and its associated ressources (flags, links, files)"""
    body = flask_rebar.get_validated_body()
    name = body["name"]
    points = body["points"]
    hidden = body["hidden"]
    description = body["description"]
    category_id = body["category_id"]

    editable_challenge = Challenge.query.filter_by(id=challenge_id).first()

    if editable_challenge is None:
        raise errors.UnprocessableEntity("This challenge does not exist.")

    if not current_admin.is_admin_of_event(editable_challenge.category.event_id):
        raise errors.Unauthorized("You do not have the permission to administer this challenge.")

    if category_id != editable_challenge.category_id:
        category = Category.query.filter_by(id=category_id, event_id=editable_challenge.category.event_id).first()

        if category is None:
            raise errors.UnprocessableEntity("The category doesn't exist.")

    if name != editable_challenge.name:
        if not name:
            raise errors.UnprocessableEntity("Name must not be empty.")

        challenge = Challenge.query.filter_by(name=name).first()

        if challenge is not None:
            raise errors.UnprocessableEntity("A challenge with that name already exists.")


    if points != editable_challenge.points and points <= 0:
        raise errors.UnprocessableEntity("Points must be positive.")

    editable_challenge.name = name
    editable_challenge.points = points
    editable_challenge.hidden = hidden
    editable_challenge.description = description
    editable_challenge.category_id = category_id

    DB.session.commit()

    return {"challenge": editable_challenge}


@REGISTRY.handles(
    rule="/admin/challenges/<int:challenge_id>",
    method="DELETE",
    response_body_schema=GenericMessageSchema()
)
@require_admin
def delete_challenge(current_admin: Administrator, challenge_id: int):
    """Delete a challenge"""

    challenge = Challenge.query.filter_by(id=challenge_id).first()

    if challenge is None:
        raise errors.UnprocessableEntity("This challenge does not exist.")

    if not current_admin.is_admin_of_event(challenge.category.event_id):
        raise errors.Unauthorized("You do not have the permission to administer this challenge.")

    # Cleanup associated ressources
    flags = Flag.query.filter_by(challenge_id=challenge_id).all()
    submissions = Submission.query.filter_by(challenge_id=challenge_id).all()

    DB.session.delete(challenge)
    DB.session.delete(flags)
    DB.session.delete(submissions)
    DB.session.commit()

    return ""
