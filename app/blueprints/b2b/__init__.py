"""
B2B Blueprint
Handles bulk orders and contracts
"""
from flask import Blueprint

b2b_bp = Blueprint('b2b', __name__, template_folder='templates')

from app.blueprints.b2b import routes
