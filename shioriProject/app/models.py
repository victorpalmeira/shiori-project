# app/models.py

import os
import jwt
from flask_login import UserMixin
from time import time
from app import db, login_manager, bcrypt


class User(UserMixin, db.Model):
    """
    Create an Employee table
    """

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(60), index=True, unique=True)
    username = db.Column(db.String(60), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    bookmarks = db.relationship('Bookmark', backref='user', lazy='dynamic')
   

    @property
    def password(self):
        """
        Prevent pasword from being accessed
        """
        raise AttributeError('password is not a readable attribute.')

    @password.setter
    def password(self, password):
        """
        Set password to a hashed password
        """
        self.password_hash = bcrypt.generate_password_hash(password)

    def verify_password(self, password):
        """
        Check if hashed password matches actual password
        """
        return bcrypt.check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User: {}>'.format(self.username)

    def get_reset_password_token(self, expires_in=600):
        return jwt.encode({'reset_password': self.id, 'exp': time() + expires_in}, os.environ['JWT_KEY'], algorithm='HS256').decode('utf-8')

    @staticmethod
    def verify_reset_password_token(token):
        try:
            id = jwt.decode(token, os.environ['JWT_KEY'], algorithms=['HS256'])['reset_password']
        except:
            return
        print('antes do id')
        print(id)
        print('depois do id')
        return User.query.get(id)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class Bookmark(db.Model):
    """
    Create a Bookmark table
    """

    __tablename__ = 'bookmarks'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), unique=True)
    url = db.Column(db.String(200))
    description = db.Column(db.String(200))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __repr__(self):
        return '<Bookmark: {}>'.format(self.name)
