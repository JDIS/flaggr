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
from JDISCTF.schemas.admin import AdminChallengeListSchema

## Missing from API
### Liste de défis
#`GET /challenges`
#-> nom de catégorie
#-> visible?
#-> *enlever completed*
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
    #authenticators=FlaskLoginAuthenticator() 
)
def get_admin_challenges(event_id: int):
    # pylint: disable=singleton-comparison
    """Get all the challenges for a given event"""
    event = Event.query.filter_by(id=event_id).first()

    if event is None:
        raise errors.NotFound(f'Event with id "{event_id}" not found.')

#    challenges = DB.session.query(Challenge).filter_by(Challenge.category.event_id == event_id).all()

    challenges = Challenge.query.join(Category).filter_by(event_id=event_id).all()

    print(challenges[0])
    print(challenges[0].category)
    return challenges
