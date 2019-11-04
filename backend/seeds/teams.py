"""Teams seeding data"""

from JDISCTF.models import Event, Team


def get_records(events: [Event]):
    """Get the records to add to the database"""
    teams = []
    for event in events:
        teams.append(Team(event_id=event.id, name='SherGill'))
        teams.append(Team(event_id=event.id, name='McBrooke'))
        teams.append(Team(event_id=event.id, name='JDIS 1'))
        teams.append(Team(event_id=event.id, name='JDIS 2'))

    return teams


FILTER_ARGS = {'event_id', 'name'}
