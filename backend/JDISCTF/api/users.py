"""Users routes"""

from flask_rebar import errors
from JDISCTF import registry
from JDISCTF.models import User
from JDISCTF.schemas import USER_SCHEMA


@registry.handles(
    rule="/users/<int:user_id>",
    method="GET",
    response_body_schema=USER_SCHEMA
)
def get_user(user_id: int):
    """Get a user's info by its id"""
    user = User.query.filter_by(id=user_id).first()

    if user is None:
        raise errors.NotFound()

    return user
