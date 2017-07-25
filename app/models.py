"""
The models module for the api
"""

from app import db
from werkzeug.security import generate_password_hash, check_password_hash


class User(db.Model):
    """
    The main user model with the users attributes
    """
    __tablename__ = 'User'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(20))
    password = db.Column(db.String(20))


    def __init__(self, email, password):
        self.email = email
        self.password = generate_password_hash(password)

    def validate_password(self, password):
        """
        Validates the user password against its hash
        """
        return check_password_hash(self.password, password)

    def add_user_data(self):
        """
        Method used for adding the users oblect to session  and committing
        """
        db.session.add(self)
        db.session.commit()


class Bucketlist(db.Model):
    """
    The main Bucketlist model and its attributes
    """
    __tablename__ = 'Bucketlist'

    pass


class Item(db.Model):
    """
    The main Item model and its attributes
    """
    __tablename__ = 'Item'

    pass
