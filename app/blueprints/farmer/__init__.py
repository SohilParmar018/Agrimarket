"""
Farmer Blueprint
Handles farmer dashboard, inventory, and analytics
"""
from flask import Blueprint

farmer_bp = Blueprint('farmer', __name__, template_folder='templates')

from app.blueprints.farmer import routes
