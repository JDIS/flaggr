"""Teams seeding data"""
from JDISCTF.models.event import Event
from JDISCTF.models.team import Team


def get_records_dev(events: [Event]):
    """Get the records to add to the database for development"""
    teams = []
    for event in events:
        teams.append(Team(event_id=event.id, name='SherGill'))
        teams.append(Team(event_id=event.id, name='McBrooke'))
        teams.append(Team(event_id=event.id, name='JDIS 1'))
        teams.append(Team(event_id=event.id, name='JDIS 2'))

    return teams


FILTER_ARGS = {'event_id', 'name'}
