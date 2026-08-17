"""
AgriMarket Application Entry Point
Initializes and runs the Flask application with SocketIO support
"""
import os
from app import create_app, socketio
from app.extensions import db

# Create Flask app instance
app = create_app(os.getenv('FLASK_ENV', 'development'))

@app.shell_context_processor
def make_shell_context():
    """
    Create shell context for Flask CLI
    Makes db and models available in flask shell
    """
    from app.models import user, product, order, message, notification, b2b_contract, sales_report
    return {
        'db': db,
        'User': user.User,
        'Product': product.Product,
        'Order': order.Order,
        'OrderItem': order.OrderItem,
        'Message': message.Message,
        'Notification': notification.Notification,
        'B2BContract': b2b_contract.B2BContract,
        'SalesReport': sales_report.SalesReport
    }

@app.cli.command()
def init_db():
    """Initialize the database with tables"""
    db.create_all()
    print("Database tables created successfully!")

@app.cli.command()
def seed_admin():
    """Create default admin user"""
    from app.models.user import User
    from werkzeug.security import generate_password_hash
    
    admin = User.query.filter_by(email='admin@agrimarket.com').first()
    if not admin:
        admin = User(
            name='Admin',
            email='admin@agrimarket.com',
            password_hash=generate_password_hash('admin123'),
            role='admin',
            phone='9999999999',
            is_verified=True,
            is_active=True
        )
        db.session.add(admin)
        db.session.commit()
        print("Admin user created: admin@agrimarket.com / admin123")
    else:
        print("Admin user already exists")

if __name__ == '__main__':
    # Run with SocketIO for real-time features
    socketio.run(
        app,
        debug=app.config['DEBUG'],
        host='0.0.0.0',
        port=5000
    )
