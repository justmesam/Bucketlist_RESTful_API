import uuid
from app import db_
from flask import request, make_response, jsonify
from flask.views import MethodView
from werkzeug.security import generate_password_hash
from app.auth import auth_blueprint
from app.models import User, LogoutDb
from app.common import email_is_valid, auth_required


class Register(MethodView):
    """
    The user register class
    """
    def post(self):
        """
        user register post method
        """
        data_ = request.get_json()
        if email_is_valid(data_.get('email')):
            user = User.query.filter_by(email=data_.get('email')).first()
            if user is not None:
                response = {
                    'message' : 'Email exists'
                }
                return make_response(jsonify(response)), 202
            else:
                user = User(data_['email'],
                            data_['password'])
                user.add_user_data()
                token_ = user.token_encoding(user.id)
                if token_:
                    response = {
                        'message' : 'You have been successfuly registered',
                        'token_' : token_.decode()
                    }
                    return make_response(jsonify(response)), 201
        else:
            response = {
                'message' : 'Wrong email format'
            }
            return make_response(jsonify(response)), 403

class Login(MethodView):
    """
    The user login class
    """
    def post(self):
        """
        user login post Method
        """
        data_ = request.get_json()
        if email_is_valid(data_.get('email')):
            user = User.query.filter_by(email=data_.get('email')).first()
            if user is None:
                response = {
                    'message' : 'You are not registered'
                }
                return make_response(jsonify(response)), 401
            elif user and user.validate_password(data_['password']):
                token_ = user.token_encoding(user.id)
                if token_:
                    response = {
                        'message' : 'Successful Login',
                        'token_' : token_.decode()
                    }
                    return make_response(jsonify(response)), 200
            else:
                response = {
                    'message' : 'Wrong email or password'
                }
                return make_response(jsonify(response)), 401
        else:
            response = {
                'message' : 'Wrong email format'
            }
            return make_response(jsonify(response)), 403


class Logout(MethodView):
    """
    The user logout class
    """
    def post(self):
        """
        user logout post method
        """
        auth_header = request.headers.get('Authorization')
        auth_token = auth_header.split("Bearer ")[1]
        if auth_token:
            auth_data = User.token_decoding(auth_token)
            if not isinstance(auth_data, str):
                logout_token = LogoutDb(auth_token)
                logout_token.save_token()
                response = {
                    'message' : 'You have successfuly logged out'
                }
                return make_response(jsonify(response)), 200
            else:
                response = {
                    'message' : auth_data
                }
                return make_response(jsonify(response)), 401
        else:
            response = {
                'message' : 'No valid token'
            }
            return make_response(jsonify(response)), 401

class Reset(MethodView):
    """
    the password reset class
    """
    def post(self):
        """
        method used to reset a users password
        """
        data_ = request.get_json()
        if email_is_valid(data_.get('email')):
            user = User.query.filter_by(email=data_.get('email')).first()
            if user:
                password = uuid.uuid4().hex
                user.password = generate_password_hash(password)
                user.add_user_data()
                response = {
                    'message' : 'Your password has been reset successfuly, you can change to a new password',
                    'new_password' : password
                }
                return make_response(jsonify(response)), 200
            else:
                response = {
                    'message' : 'Email do not exist'
                }
                return make_response(jsonify(response)), 401
        else:
            response = {
                'message' : 'Wrong email format'
            }
            return make_response(jsonify(response)), 403

class ChangePassword(MethodView):
    """
    class used for changing password
    """
    @auth_required
    def post(self, auth_data):
        data_ = request.get_json()
        user = User.query.filter_by(id=auth_data).first()
        old_password = data_.get('old_password')
        new_password = data_.get('new_password')
        confirm_password = data_.get('confirm_password')
        if old_password and user.validate_password(old_password):
            if new_password == confirm_password:
                user.password = generate_password_hash(new_password)
                user.add_user_data()
                response = {
                    'message' : 'You have changed the password successfuly'
                }
                return make_response(jsonify(response)), 200
            else:
                response = {
                    'message' : 'New password and Confirm password should be equal'
                }
                return make_response(jsonify(response)), 400
        else:
            response = {
                'message' : 'Wrong  password'
            }
            return make_response(jsonify(response)), 401

class DeleteUser(MethodView):
    """
    class used for deleting an user
    """
    @auth_required
    def post(self, auth_data):
        data_ = request.get_json()
        password = data_.get('password')
        user = User.query.filter_by(id=auth_data).first()
        if password and user.validate_password(password):
            db_.session.delete(user)
            db_.session.commit()
            response = {
                'message' : 'User successfuly deleted'
            }
            return make_response(jsonify(response)), 200
        else:
            response = {
                'message' : 'Wrong  password'
            }
            return make_response(jsonify(response)), 401


auth_blueprint.add_url_rule('/register/',
                            view_func=Register.as_view('register'),
                            methods=['POST'])
auth_blueprint.add_url_rule('/login/',
                            view_func=Login.as_view('login'),
                            methods=['POST'])
auth_blueprint.add_url_rule('/logout/',
                            view_func=Logout.as_view('logout'),
                            methods=['POST'])
auth_blueprint.add_url_rule('/reset_password/',
                            view_func=Reset.as_view('reset'),
                            methods=['POST'])
auth_blueprint.add_url_rule('/change_password/',
                            view_func=ChangePassword.as_view('change_password'),
                            methods=['POST'])
auth_blueprint.add_url_rule('/delete/',
                            view_func=DeleteUser.as_view('delete'),
                            methods=['POST'])
