"""'Categories' SQLAlchemy model"""

from JDISCTF.app import DB
from sqlalchemy import ForeignKey, UniqueConstraint


class Category(DB.Model):
    """Category model"""
    id = DB.Column(DB.Integer, primary_key=True)
    __tablename__ = 'Categories'

    event_id = DB.Column(DB.Integer, ForeignKey('Events.id'), nullable=True)
    name = DB.Column(DB.String(64), index=True)

    __table_args__ = \
        (
            UniqueConstraint('event_id', 'name', name='_event_name_uc'),
        )

    def __repr__(self):
        return '<Category id:{} event_id:{} name:{}'.format(self.id, self.event_id, self.name)
