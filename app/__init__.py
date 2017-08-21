import os
from flask import Flask, make_response, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db_ = SQLAlchemy()
db_.init_app(app)

from app.auth import auth_blueprint
from app.bucketlist import bucketlist_blueprint
from app.item import item_blueprint
from app.models import Bucketlist, Item, User


@app.route('/search/', methods=['GET'])
def search_api():
    auth_header = request.headers.get('Authorization')
    auth_token = auth_header.split("Bearer ")[1]
    if auth_token:
        auth_data = User.token_decoding(auth_token)
        if not isinstance(auth_data, str):
            search = request.args.get('q', type=str)
            if not search:
                response = {
                    'message' : 'Enter a search parameter'
                }
                return make_response(jsonify(response)), 404
            else:
                bucketlist_found = Bucketlist.query.filter_by(owner=auth_data).\
                 filter(Bucketlist.title.contains(search)).all()
                all_bucketlists = []
                for bucketlist in bucketlist_found:
                    items = Item.query_items(bucketlist.id)
                    all_items = []
                    for item in items:
                        obj = item.serialize()
                        all_items.append(obj)
                        bucketlist_ = bucketlist.serialize()
                        bucketlist_['items'] = all_items
                    all_bucketlists.append(bucketlist_)
                return make_response(jsonify(bucketlists=all_bucketlists)), 200
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

app.register_blueprint(auth_blueprint, url_prefix='/auth')
app.register_blueprint(bucketlist_blueprint, url_prefix='/bucketlists')
app.register_blueprint(item_blueprint, url_prefix='/bucketlists')
