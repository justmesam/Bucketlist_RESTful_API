from flask import json
from flask import request, make_response, jsonify
from flask.views import MethodView
from app.auth import auth_blueprint
from app.models import User


class Register(MethodView):
    """
    The user register class
    """
    def post(self):
        data_ = json.loads(request.data.decode())
        user = User.query.filter_by(email=data_['email']).first()
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
        data_ = json.loads(request.data.decode())
        user = User.query.filter_by(email=data_['email']).first()
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

auth_blueprint.add_url_rule('/auth/register',
                            view_func=Register.as_view('register'),
                            methods=['POST'])
auth_blueprint.add_url_rule('/auth/login',
                            view_func=Login.as_view('login'),
                            methods=['POST'])
