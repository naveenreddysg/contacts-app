from db import db

"""
    INITIALISE MODEL FOR CONTACTS TABLE
"""

class ContactModel(db.Model):

    __tablename__ = 'contacts'

    id = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
    name = db.Column('name', db.String(64))
    email = db.Column('email', db.String(99))
    mobile = db.Column('mobile', db.String(16))
    phone = db.Column('phone', db.String(16))
    createdOn = db.Column('created_on', db.DateTime)
    updatedOn = db.Column('updated_on', db.DateTime)