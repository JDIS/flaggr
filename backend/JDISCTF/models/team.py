"""Teams' SQLAlchemy model"""

from __future__ import annotations
from JDISCTF.app import DB
from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship

class Team(DB.Model):
    """Team model"""
    id = DB.Column(DB.Integer, primary_key=True)
    __tablename__ = 'Teams'
    __table_args__ = (
        UniqueConstraint('event_id', 'name', name='team_event_name_uc'),
    )

    event_id = DB.Column(DB.Integer, ForeignKey('Events.id'), nullable=True)
    name = DB.Column(DB.String(64), index=True)

    members = relationship('TeamMember', lazy="joined", back_populates="team")
    requests = relationship('TeamRequest', lazy='noload')

    def __repr__(self):
        return '<Team id:{} event_id:{} name:{}>'.format(self.id, self.event_id, self.name)


class TeamMember(DB.Model):
    """TeamMember model"""
    id = DB.Column(DB.Integer, primary_key=True)
    __tablename__ = 'TeamMembers'

    team_id = DB.Column(DB.Integer, ForeignKey('Teams.id'), nullable=True)
    user_id = DB.Column(DB.Integer, ForeignKey('Users.id'), nullable=True)

    # Let a team have many captain, since a captain can accept members
    captain = DB.Column(DB.Boolean)

    team = relationship("Team", back_populates="members")
    user = relationship("User",)
    
    def __repr__(self): 
        return '<TeamMember id:{} team_id:{} user_id:{}>'.format(self.id, self.team_id, self.user_id)


class TeamRequest(DB.Model):
    """TeamRequest model"""
    id = DB.Column(DB.Integer, primary_key=True)
    __tablename__ = 'TeamRequests'

    team_id = DB.Column(DB.Integer, ForeignKey('Teams.id'), nullable=True)
    user_id = DB.Column(DB.Integer, ForeignKey('Users.id'), nullable=True)
    requested_at = DB.Column(DB.DateTime, server_default=DB.func.now())

    def __repr__(self):
        return '<TeamRequests id:{} team_id:{} user_id:{}>'.format(self.id, self.team_id, self.user_id)


def load_team(user_id: int) -> Team:
    team = None
    #team = TeamMember.query(user_id=user_id).first()
    return team