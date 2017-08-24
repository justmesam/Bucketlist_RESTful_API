import re
from functools import wraps
from flask import make_response, jsonify, request
from app.models import User


def auth_required(func):
    """
    decorator method for verifying authentication
    """
    @wraps(func)
    def check_token(*args, **kwargs):
        """
        token decoding
        """
        auth_header = request.headers.get('Authorization')
        auth_token = auth_header.split("Bearer ")[1]
        if auth_token:
            auth_data = User.token_decoding(auth_token)
            if not isinstance(auth_data, str):
                auth_data = auth_data
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
        return func(auth_data=auth_data, *args, **kwargs)
    return check_token


def email_is_valid(email):
    """
    checks if an email is valid
    """
    if len(email) > 8:
        email_match = re.compile\
         (r'^[\w-]+@([\w-]+\.)+[\w]+$')
        return True if email_match.match(email) else False
    return False
