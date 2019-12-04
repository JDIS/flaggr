"""EventAdministrators seeding data"""

from JDISCTF.models import Event, Administrator, EventAdministrator


def get_records(admins: [Administrator], events: [Event]):
    """Get the records to add to the database"""
    event_admins = [EventAdministrator(event_id=events[0].id, administrator_id=admins[0].id),
                    EventAdministrator(event_id=events[0].id, administrator_id=admins[1].id),
                    EventAdministrator(event_id=events[1].id, administrator_id=admins[0].id),
                    EventAdministrator(event_id=events[1].id, administrator_id=admins[1].id),
                    EventAdministrator(event_id=events[2].id, administrator_id=admins[2].id),
                    EventAdministrator(event_id=events[2].id, administrator_id=admins[3].id),
                    EventAdministrator(event_id=events[3].id, administrator_id=admins[2].id),
                    EventAdministrator(event_id=events[3].id, administrator_id=admins[3].id)]

    return event_admins


FILTER_ARGS = {'event_id', 'administrator_id'}
