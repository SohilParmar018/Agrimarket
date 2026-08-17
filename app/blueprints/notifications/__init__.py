"""
Notifications Blueprint
Handles real-time notifications
"""
from flask import Blueprint

notifications_bp = Blueprint('notifications', __name__, template_folder='templates')

from app.blueprints.notifications import routes
