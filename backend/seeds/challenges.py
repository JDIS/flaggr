"""Challenges seeding data"""

from JDISCTF.models import Category, Challenge


def get_records_dev(categories: [Category]):
    """Get the records to add to the database for development"""
    challenges = []
    for category in categories:
        challenges.append(Challenge(category_id=category.id, name='Super Duper Challenge',
                                    description='## title 2\n\nA **really** *cool* challenge for'
                                                'everyone https://google.ca', points=50,
                                    hidden=False))
        challenges.append(Challenge(category_id=category.id, name='Pretty hard challenge',
                                    description='A pretty hard challenge for veterans', points=100,
                                    hidden=True))
        challenges.append(Challenge(category_id=category.id,
                                    name="You Better Know What You're Doing Challenge",
                                    description='A challenge for very specific skill sets',
                                    points=300, hidden=False))
        challenges.append(Challenge(category_id=category.id,
                                    name='Hope You Had Nothing Else To Do Challenge',
                                    description='A challenge that takes a whole week', points=5000,
                                    hidden=True))

    return challenges


FILTER_ARGS = {'category_id', 'name'}
