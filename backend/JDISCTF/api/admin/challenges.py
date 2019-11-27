"""Challenges routes"""
import re

import flask_rebar
from flask_login import current_user
from flask_rebar import errors
from sqlalchemy.orm import contains_eager

from JDISCTF.app import DB, REGISTRY
from JDISCTF.flask_login_authenticator import FlaskLoginAuthenticator
from JDISCTF.models import Category, Challenge, Event, Flag, Submission
from JDISCTF.schemas import ChallengeByCategorySchema, SubmitFlagResponseSchema, \
    SubmitFlagSchema, UserChallengeSchema

from JDISCTF.schemas.admin import AdminChallengeInformationSchema, AdminChallengeListSchema

## Missing from API
#
### Édition/Modification de défi
#`GET /challenges/:id`
#-> nom
#-> trackId
#-> tags
#-> flag
#-> points
#-> description
#-> files
#-> links
#`POST /challenges`
#`PUT /challenges/:id`
#`DELETE /challenges/:id`
#`GET /tracks`
#`POST /tracks`

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

    if challenge is None:
        raise errors.NotFound(f'Challenge with id "{challenge_id}" not found.')

    # FIXME Missing validations. If the current admin is admin of challenge.category.event_id

    return {"challenge": challenge, "flags": flags}