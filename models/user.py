from db import db


class UserModel(db.Model):
    """
    Represents a user in the system.

    :Attributes:
        :id (int): The primary key representing a unique user entry.
        :username (str): The username of the user, which must be unique and cannot be null.
        :password (str): The hashed password of the user, which cannot be null.
    """
    
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
