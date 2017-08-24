import os
from functools import wraps
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
from app.common import auth_required


@app.route('/search/', methods=['GET'])
@auth_required
def search_api(auth_data, *args, **kwargs):
    """
    method for searching bucketlist by name/title
    """
    search = request.args.get('q', type=str)
    if not search:
        response = {
            'message' : 'Enter a search parameter'
        }
        return make_response(jsonify(response)), 404
    else:
        bucketlist_found = Bucketlist.query.filter_by(owner=auth_data).\
         filter(Bucketlist.title.contains(search)).all()
        all_bucketlists = [bucketlist.serialize() for bucketlist in bucketlist_found]
        for bucketlist in all_bucketlists:
            bucketlist.update(
                {"items" : [item.serialize()\
                 for item in Item.query_items(bucketlist['id'])]}
            )
        return make_response(jsonify(bucketlists=all_bucketlists)), 200

app.register_blueprint(auth_blueprint, url_prefix='/auth')
app.register_blueprint(bucketlist_blueprint, url_prefix='/bucketlists')
app.register_blueprint(item_blueprint, url_prefix='/bucketlists')
