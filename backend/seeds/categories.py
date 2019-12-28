"""Categories seeding data"""

from JDISCTF.models import Category, Event


def get_records_dev(events: [Event]):
    """Get the records to add to the database for development"""
    categories = []
    for event in events:
        categories.append(Category(event_id=event.id, name='Web'))
        categories.append(Category(event_id=event.id, name='Forensics'))
        categories.append(Category(event_id=event.id, name='Steg'))
        categories.append(Category(event_id=event.id, name='Programming'))

    return categories


FILTER_ARGS = {'event_id', 'name'}
