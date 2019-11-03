"""Flags seeding data"""

from JDISCTF.models import Flag, Challenge


def get_records(challenges: [Challenge]):
    """Get the records to add to the database"""
    flags = []
    for challenge in challenges:
        flags.append(Flag(challenge_id=challenge.id, is_regex=False, value='flag-JDIS'))
        flags.append(Flag(challenge_id=challenge.id, is_regex=True, value='regex-*'))

    return flags


FILTER_ARGS = {'challenge_id', 'is_regex', 'value'}
