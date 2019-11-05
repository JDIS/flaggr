"""'Events' SQLAlchemy model"""

from JDISCTF.app import DB


class Event(DB.Model):
    """
    Event model

    The core of the application. An event's only defining characteristic is its name, which must be
    unique (i.e. 'CS Games 2019', 'United CTF 2019', etc). The rest is all handled by relations with
    the application's other models.
    """

    __tablename__ = 'Events'

    id = DB.Column(DB.Integer, primary_key=True)
    """The unique ID of the event. Should be generated by the database. Used as primary key."""
    name = DB.Column(DB.String(64), index=True, unique=True)
    """The name of the event. Max 64 characters."""
    teams = DB.Column(DB.Boolean)
    """Whether participants have to register as teams or individually."""

    def __repr__(self):
        return '<Event id:{} name:{} teams: {}'.format(self.id, self.name, self.teams)