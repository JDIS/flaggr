"""Users routes"""

from flask_login import current_user
from flask_rebar import errors

from JDISCTF.app import REGISTRY
from JDISCTF.models import User
from JDISCTF.schemas import UserSchema


@REGISTRY.handles(
    rule="/user",
    method="GET",
    response_body_schema=UserSchema()
)
def get_connected_user():
    """Get the connected user."""
    return current_user


@REGISTRY.handles(
    rule="/users",
    method="GET",
    response_body_schema=UserSchema(many=True),
    authenticators=None
)
def get_all_users():
    """DEVELOPMENT ROUTE. Gets all the users, non-paginated"""
    user = User.query.all()

    return user


@REGISTRY.handles(
    rule="/users/<int:user_id>",
    method="GET",
    response_body_schema=UserSchema(),
    authenticators=None
)
def get_user(user_id: int):
    """Get a user's info by its id"""
    user = User.query.filter_by(id=user_id).first()

    if user is None:
        raise errors.NotFound()

    return user
