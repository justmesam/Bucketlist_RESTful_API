import os
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db_ = SQLAlchemy()
db_.init_app(app)

from app.auth import auth_blueprint
app.register_blueprint(auth_blueprint)
