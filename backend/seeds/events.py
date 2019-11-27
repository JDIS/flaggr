"""Events seeding data"""

from JDISCTF.models import Event


def get_records():
    """Get the records to add to the database"""
    return [
        Event(name='CS Games 2019', teams=True, id=0, front_page='#CS Games 2019'),
        Event(name='JDIS Games 2019', teams=True, front_page='#JDISGames 2019'),
        Event(name='Pico CTF 2019', teams=False, front_page='#PicoCTF 2019'),
        Event(name='United CTF 2019', teams=False, front_page='#UnitedCTF 2019')
    ]


FILTER_ARGS = {'name'}
