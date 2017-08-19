from flask import request, make_response, jsonify, json
from flask.views import MethodView
from app.auth import auth_blueprint
from app.models import User, LogoutDb


class Register(MethodView):
    """
    The user register class
    """
    def post(self):
        """
        user register post method
        """
        data_ = request.get_json()
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

class Login(MethodView):
    """
    The user login class
    """
    def post(self):
        """
        user login post Method
        """
        data_ = request.get_json()
        user = User.query.filter_by(email=data_.get('email')).first()
        if user is None:
            response = {
                'message' : 'You are not reqistered'
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
    method used to reset a users password
    """
    def post(self):
        pass


auth_blueprint.add_url_rule('/register',
                            view_func=Register.as_view('register'),
                            methods=['POST'])
auth_blueprint.add_url_rule('/login',
                            view_func=Login.as_view('login'),
                            methods=['POST'])
auth_blueprint.add_url_rule('/logout',
                            view_func=Logout.as_view('logout'),
                            methods=['POST'])
