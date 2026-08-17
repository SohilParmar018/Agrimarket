"""
Messaging Blueprint
Handles real-time messaging between users
"""
from flask import Blueprint

messaging_bp = Blueprint('messaging', __name__, template_folder='templates')

from app.blueprints.messaging import routes
