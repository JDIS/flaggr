from JDISCTF import db
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
    __tablename__ = 'Users'
    id = db.Column(db.Integer, primary_key=True)

    email = db.Column(db.String(255), index=True, unique=True)
    username = db.Column(db.String(64), index=True, unique=True)
    password_hash = db.Column(db.String(128))

    def __repr__(self):
        return '<User id:{} user:{} email:{}>'.format(self.id, self.username, self.email)