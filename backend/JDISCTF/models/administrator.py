"""'Administrator's SQLAlchemy model"""

from flask_login import UserMixin
from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.orm import relationship

from JDISCTF.app import DB
from JDISCTF.models.role import Role


class Administrator(UserMixin, DB.Model):
    """
    Administrator model

    An administrator is a person who manages events. Depending on his roles, an administrator can
    create challenge, edit event info, edit event theme, etc. Administrators use a single account to
    manage all events.
    """

    __tablename__ = 'Administrators'

    id = DB.Column(DB.Integer, primary_key=True)
    """The unique ID of the admin. Should be generated by the database. Used as primary key."""
    is_platform_admin = DB.Column(DB.Boolean)
    """
    Defines whether or not the administrator is a platform admin. Platform admins have complete
    to all of the platform's configuration as well as all events.
    """
    user_id = DB.Column(DB.Integer, ForeignKey('Users.id'), nullable=True, unique=True)
    """The ID of the event the administrator is associated with. Used as a foreign key."""

    event_administrators = relationship('EventAdministrator')
    events = association_proxy('event_administrators', 'event')

    user = relationship('User', lazy='joined')

    def is_admin_of_event(self, event_id: int) -> bool:
        """
        :param event_id:
        :return: True if the admin is admin for the given event.
        """
        return self.is_platform_admin or event_id in map(lambda x: x.id, self.events)

    def get_roles_for_event(self, event_id: int) -> [Role]:
        """
        :param event_id:
        :return: The list of all the roles the administrator has for the given event.
        """
        event_administrators = filter(lambda x: x.event_id == event_id, self.event_administrators)
        roles = map(lambda x: x.roles, event_administrators)
        return set().union(*roles)

    def __repr__(self):
        return '<Administrator id:{} is_platform_admin:{} user_id:{}>' \
            .format(self.id, self.is_platform_admin, self.user_id)


class EventAdministrator(DB.Model):
    """
    EventAdministrators model. This is an association table between administrators and events.
    """
    __tablename__ = 'EventAdministrators'

    id = DB.Column(DB.Integer, primary_key=True)
    """The unique ID of the row. Should be generated by the database. Used as primary key."""
    event_id = DB.Column(DB.Integer, ForeignKey('Events.id'), nullable=True)
    """The ID of the Event that this row associates. Used as foreign key."""
    administrator_id = DB.Column(DB.Integer, ForeignKey('Administrators.id'), nullable=True)
    """The ID of the Administrator that this row associates. Used as foreign key."""

    event = relationship('Event', back_populates='event_administrators', lazy='joined')
    administrator = relationship('Administrator', back_populates='event_administrators', lazy='joined')
    roles = relationship('RoleAssociation', back_populates='event_administrator', lazy='joined')

    __table_args__ = (
        UniqueConstraint('event_id', 'administrator_id', name='event_administrator_event_administrator_uc'),
    )

    def __repr__(self):
        return '<EventAdministrator id:{} event_id:{} administrator_id:{}>' \
            .format(self.id, self.event_id, self.administrator_id)
