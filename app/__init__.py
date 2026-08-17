"""
AgriMarket Application Factory
Creates and configures the Flask application with all extensions and blueprints
"""
from flask import Flask, render_template
from app.config import config
from app.extensions import db, login_manager, migrate, socketio, mail, jwt


def create_app(config_name='development'):
    """
    Application factory pattern
    
    Args:
        config_name: Configuration to use (development/production/testing)
    
    Returns:
        Configured Flask application instance
    """
    app = Flask(__name__)
    
    # Load configuration
    app.config.from_object(config[config_name])
    
    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)
    # Use threading mode for better compatibility (change to 'gevent' or 'eventlet' if installed)
    socketio.init_app(app, cors_allowed_origins="*", async_mode='threading')
    mail.init_app(app)
    jwt.init_app(app)
    
    # Configure login manager
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Please log in to access this page.'
    login_manager.login_message_category = 'info'
    
    @login_manager.user_loader
    def load_user(user_id):
        from app.models.user import User
        return User.query.get(int(user_id))
    
    # Register blueprints
    register_blueprints(app)
    
    # Register error handlers
    register_error_handlers(app)
    
    # Register template filters
    register_template_filters(app)
    
    # Create upload directories
    import os
    upload_folder = app.config.get('UPLOAD_FOLDER', 'app/static/uploads')
    os.makedirs(upload_folder, exist_ok=True)
    os.makedirs(os.path.join(upload_folder, 'products'), exist_ok=True)
    os.makedirs(os.path.join(upload_folder, 'profiles'), exist_ok=True)
    os.makedirs(os.path.join(upload_folder, 'contracts'), exist_ok=True)
    
    return app


def register_blueprints(app):
    """Register all application blueprints"""
    # Import blueprints
    from app.blueprints.auth import auth_bp
    from app.blueprints.farmer import farmer_bp
    from app.blueprints.buyer import buyer_bp
    from app.blueprints.orders import orders_bp
    from app.blueprints.messaging import messaging_bp
    from app.blueprints.notifications import notifications_bp
    from app.blueprints.b2b import b2b_bp
    from app.blueprints.reports import reports_bp
    from app.blueprints.admin import admin_bp
    
    # Register blueprints
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(farmer_bp, url_prefix='/farmer')
    app.register_blueprint(buyer_bp, url_prefix='/buyer')
    app.register_blueprint(orders_bp, url_prefix='/orders')
    app.register_blueprint(messaging_bp, url_prefix='/messages')
    app.register_blueprint(notifications_bp, url_prefix='/notifications')
    app.register_blueprint(b2b_bp, url_prefix='/b2b')
    app.register_blueprint(reports_bp, url_prefix='/reports')
    app.register_blueprint(admin_bp, url_prefix='/admin')
    
    # Home route
    @app.route('/')
    def index():
        return render_template('index.html')


def register_error_handlers(app):
    """Register error handlers for common HTTP errors"""
    
    @app.errorhandler(404)
    def not_found_error(error):
        return render_template('errors/404.html'), 404
    
    @app.errorhandler(403)
    def forbidden_error(error):
        return render_template('errors/403.html'), 403
    
    @app.errorhandler(500)
    def internal_error(error):
        db.session.rollback()
        return render_template('errors/500.html'), 500
    
    @app.errorhandler(413)
    def request_entity_too_large(error):
        return render_template('errors/413.html'), 413


def register_template_filters(app):
    """Register custom Jinja2 template filters"""
    
    @app.template_filter('currency')
    def currency_filter(value):
        """Format number as Indian currency"""
        try:
            return f"₹{value:,.2f}"
        except (ValueError, TypeError):
            return value
    
    @app.template_filter('datetime')
    def datetime_filter(value, format='%d %b %Y, %I:%M %p'):
        """Format datetime object"""
        if value is None:
            return ""
        return value.strftime(format)
    
    @app.template_filter('status_badge')
    def status_badge_filter(status):
        """Return Bootstrap badge class for order status"""
        badge_map = {
            'pending': 'warning',
            'confirmed': 'info',
            'processing': 'primary',
            'shipped': 'secondary',
            'delivered': 'success',
            'cancelled': 'danger'
        }
        return badge_map.get(status, 'secondary')
