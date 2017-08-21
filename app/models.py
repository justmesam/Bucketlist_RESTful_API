"""
The models module for the api
"""
import datetime
import jwt
from flask import current_app
from werkzeug.security import generate_password_hash, check_password_hash
from . import db_


class User(db_.Model):
    """
    The main user model with the users attributes
    """
    __tablename__ = 'User'

    id = db_.Column(db_.Integer, primary_key=True)
    email = db_.Column(db_.String(300))
    password = db_.Column(db_.String(300))
    bucketlists = db_.relationship(
        "Bucketlist", order_by="Bucketlist.id", cascade="all, delete-orphan"
    )


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
            if LogoutDb.verify(token_):
                return 'Please Login'
            else:
                return payload['sub']
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
    owner = db_.Column(db_.Integer, db_.ForeignKey(User.id))
    date_created = db_.Column(db_.DateTime, default=db_.func.current_timestamp())
    date_updated = db_.Column(db_.DateTime, default=db_.func.current_timestamp(),
                              onupdate=db_.func.current_timestamp())
    items = db_.relationship("Item", order_by="Item.id", cascade="all, delete-orphan")

    def __init__(self, title, intro, owner):
        self.title = title
        self.intro = intro
        self.owner = owner

    def save_bucketlist(self):
        """
        method used for saving the bucketlists to DATABASE
        """
        db_.session.add(self)
        db_.session.commit()

    @staticmethod
    def query_all(owner_id):
        """
        method used for querying all the bucketlists from the database using an
        owner id
        """
        all_bucketlists = Bucketlist.query.filter_by(owner=owner_id)
        return all_bucketlists

    def delete(self):
        """
        method used for deleting bucketlists
        """
        db_.session.delete(self)
        db_.session.commit()

    def serialize(self):
        """
        returns the object as dictionary
        """
        return {
            'id' : self.id,
            'owner' : self.owner,
            'date_created' : self.date_created,
            'date_updated' : self.date_updated,
            'title' : self.title,
            'intro' : self.intro
        }

class LogoutDb(db_.Model):
    """
    This model is used to store tokens
    """

    id = db_.Column(db_.Integer, primary_key=True)
    token = db_.Column(db_.String(300))
    logout_time = db_.Column(db_.DateTime, default=db_.func.current_timestamp())

    def __init__(self, token):
        self.token = token

    def save_token(self):
        """
        method used for saving the token to database
        """
        db_.session.add(self)
        db_.session.commit()

    @staticmethod
    def verify(token_):
        """
        checks if the token exists in the database where all logged out tokens are
        """
        response = LogoutDb.query.filter_by(token=str(token_)).first()
        if response:
            return True
        else:
            return False


class Item(db_.Model):
    """
    The main Item model and its attributes
    """
    __tablename__ = 'Item'

    id = db_.Column(db_.Integer, primary_key=True)
    title = db_.Column(db_.String(300))
    intro = db_.Column(db_.String(500))
    date_created = db_.Column(db_.DateTime, default=db_.func.current_timestamp())
    date_updated = db_.Column(db_.DateTime, default=db_.func.current_timestamp(),
                              onupdate=db_.func.current_timestamp())
    owner = db_.Column(db_.Integer, db_.ForeignKey(Bucketlist.id))

    def __init__(self, title, intro, owner):
        self.title = title
        self.intro = intro
        self.owner = owner

    @staticmethod
    def query_items(owner_id):
        """
        method used to query all items from the database using the owners id
        """
        all_items = Item.query.filter_by(owner=owner_id)
        return all_items

    def save_item(self):
        """
        method used to save items to the database
        """
        db_.session.add(self)
        db_.session.commit()

    def delete(self):
        """
        method used for deleting items
        """
        db_.session.delete(self)
        db_.session.commit()

    def serialize(self):
        """
        returns the object as dictionary
        """
        return {
            'id' : self.id,
            'owner' : self.owner,
            'date_created' : self.date_created,
            'date_updated' : self.date_updated,
            'title' : self.title,
            'intro' : self.intro
        }
