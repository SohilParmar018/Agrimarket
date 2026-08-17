"""
Admin Blueprint
Handles admin panel and platform management
"""
from flask import Blueprint

admin_bp = Blueprint('admin', __name__, template_folder='templates')

from app.blueprints.admin import routes
