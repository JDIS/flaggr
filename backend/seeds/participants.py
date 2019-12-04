"""Participants seeding data"""

from JDISCTF.models import Participant, User, Event


def get_records(users: [User], events: [Event]):
    """Get the records to add to the database"""
    participants = []
    for i, event in enumerate(events):
        for j in range(4):
            participants.append(Participant(user_id=users[i * 4 + j].id, event_id=event.id))

    return participants


FILTER_ARGS = {'user_id', 'event_id'}
