"""Participants seeding data"""

from JDISCTF.models import Participant, User, Event


def get_records(users: [User], events: [Event]):
    """Get the records to add to the database"""
    participants = []
    for event in events:
        for user in users:
            participants.append(Participant(user_id=user.id, event_id=event.id))

    return participants


FILTER_ARGS = {'user_id', 'event_id'}
