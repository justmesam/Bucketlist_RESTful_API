"""
The models module for the api
"""
from . import db_
import datetime
import jwt
from flask import current_app
from werkzeug.security import generate_password_hash, check_password_hash


class User(db_.Model):
    """
    The main user model with the users attributes
    """
    __tablename__ = 'User'

    id = db_.Column(db_.Integer, primary_key=True)
    email = db_.Column(db_.String(300))
    password = db_.Column(db_.String(300))


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
        db_.session.add(self)
        db_.session.commit()

    def token_encoding(self, _id):
        """
        Generates the token_
        :return:string
        """
        try:
            payload = {'exp': datetime.datetime.utcnow() + datetime.timedelta(days=0,
                                                                              hours=1),
                       'iat': datetime.datetime.utcnow(),
                       'sub': _id
                      }
            return jwt.encode(payload,
                              current_app.config.get('SECRET_KEY'),
                              algorithm='HS256')
        except Exception as e:
            return e

    @staticmethod
    def token_decoding(token_):
        """
        Decode the token_
        :param token_:
        :return:string|integer:
        """
        try:
            payload = jwt.decode(token_, current_app.config.get('SECRET_KEY'))
        except jwt.ExpiredSignatureError:
            return 'Signature is expired, try to login'
        except jwt.InvalidTokenError:
            return 'Invalid token, try to login'

class Bucketlist(db_.Model):
    """
    The main Bucketlist model and its attributes
    """
    __tablename__ = 'Bucketlist'

    id = db_.Column(db_.Integer, primary_key=True)
    title = db_.Column(db_.String(300))
    intro = db_.Column(db_.String(500))

    def __init__(self, title, intro):
        self.title = title
        self.intro = intro

"""
class Item(db_.Model):
    """
    The main Item model and its attributes
    """
    __tablename__ = 'Item'

    pass
'''
