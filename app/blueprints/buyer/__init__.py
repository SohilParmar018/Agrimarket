"""
Buyer Blueprint
Handles buyer dashboard, product browsing, and orders
"""
from flask import Blueprint

buyer_bp = Blueprint('buyer', __name__, template_folder='templates')

from app.blueprints.buyer import routes
