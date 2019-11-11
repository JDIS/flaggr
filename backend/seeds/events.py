"""Events seeding data"""

from JDISCTF.models import Event


def get_records():
    """Get the records to add to the database"""
    return [
        Event(name='CS Games 2019', teams=True, id=0),
        Event(name='JDIS Games 2019', teams=True),
        Event(name='Pico CTF 2019', teams=False),
        Event(name='United CTF 2019', teams=False)
    ]


FILTER_ARGS = {'name'}
