import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db_ = SQLAlchemy()
db_.init_app(app)


from app.auth import auth_blueprint
from app.bucketlist import bucketlist_blueprint
from app.item import item_blueprint
app.register_blueprint(auth_blueprint, url_prefix='/auth')
app.register_blueprint(bucketlist_blueprint, url_prefix='/bucketlists')
app.register_blueprint(item_blueprint, url_prefix='/bucketlists')
