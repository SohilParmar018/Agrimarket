"""
Flask Extensions
Initializes all Flask extensions used in the application
"""
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_socketio import SocketIO
from flask_mail import Mail
from flask_jwt_extended import JWTManager

# Database ORM
db = SQLAlchemy()

# User session management
login_manager = LoginManager()

# Database migrations
migrate = Migrate()

# Real-time communication
socketio = SocketIO()

# Email sending
mail = Mail()

# JWT token management
jwt = JWTManager()
