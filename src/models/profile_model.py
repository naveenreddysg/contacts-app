from db import db

"""
    INITIALISE MODEL FOR PROFILE TABLE
"""

class ProfileModel(db.Model):

    __tablename__ = 'profile'

    id = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
    name = db.Column('name', db.String(64))
    email = db.Column('email', db.String(99))
    password = db.Column('password', db.Text)
    createdOn = db.Column('created_on', db.DateTime)
    updatedOn = db.Column('updated_on', db.DateTime)