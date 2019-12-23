"""Administrators seeding data"""

from JDISCTF.models import Administrator, User


def get_records_dev(users: [User]):
    """Get the records to add to the database for development"""
    admins = [Administrator(is_platform_admin=True, user_id=users[len(users) - 4].id),
              Administrator(is_platform_admin=True, user_id=users[len(users) - 3].id),
              Administrator(is_platform_admin=False, user_id=users[len(users) - 2].id),
              Administrator(is_platform_admin=False, user_id=users[len(users) - 1].id)]

    return admins


FILTER_ARGS = {'user_id'}
