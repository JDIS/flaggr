"""User model"""

from __future__ import annotations
from JDISCTF import db
from werkzeug.security import generate_password_hash, check_password_hash


class User(db.Model):
    """User model"""
    id = db.Column(db.Integer, primary_key=True)
    __tablename__ = 'Users'

    email = db.Column(db.String(255), index=True, unique=True)
    username = db.Column(db.String(64), index=True, unique=True)
    password_hash = db.Column(db.String(128))

    def __repr__(self):
        return '<User id:{} email:{} username:{}>'.format(self.id, self.email, self.username)

    def set_password(self, password: str):
        """Hash and set the user's password"""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        """Check whether or not this is the user's password"""
        return check_password_hash(self.password_hash, password)
