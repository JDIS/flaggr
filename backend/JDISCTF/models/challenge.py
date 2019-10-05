"""'Challenges' SQLAlchemy model"""

from JDISCTF.app import DB
from sqlalchemy import ForeignKey


class Challenge(DB.Model):
    """Challenge model"""
    id = DB.Column(DB.Integer, primary_key=True)
    __tablename__ = 'Challenges'

    category_id = DB.Column(DB.Integer, ForeignKey('Categories.id'), nullable=True)
    name = DB.Column(DB.String(255), index=True)
    description = DB.Column(DB.Text())
    points = DB.Column(DB.Integer)
    hidden = DB.Column(DB.Boolean)

    def __repr__(self):
        return '<Challenge id:{} category_id:{} name:{} description:{} points:{}'\
            .format(self.id, self.category_id, self.name, self.description, self.points)
