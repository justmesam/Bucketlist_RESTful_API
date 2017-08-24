"""
This module initializes the item blueprint
"""
from flask import Blueprint

item_blueprint = Blueprint('item', __name__)

from . import views
