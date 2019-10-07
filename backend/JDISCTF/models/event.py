"""'Events' SQLAlchemy model"""

from JDISCTF.app import DB


class Event(DB.Model):
    """Event model"""
    id = DB.Column(DB.Integer, primary_key=True)
    __tablename__ = 'Events'

    name = DB.Column(DB.String(64), index=True, unique=True)
    teams = DB.Column(DB.Boolean)

    def __repr__(self):
        return '<Category id:{} name:{} teams: {}'.format(self.id, self.name, self.teams)
