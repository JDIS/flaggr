"""Participants seeding data"""

from JDISCTF.models import Event, Participant, User


def get_records_dev(users: [User], events: [Event]):
    """Get the records to add to the database for development"""
    participants = []
    for i, event in enumerate(events):
        for j in range(4):
            participants.append(Participant(user_id=users[i * 4 + j].id, event_id=event.id))

    return participants


FILTER_ARGS = {'user_id', 'event_id'}
