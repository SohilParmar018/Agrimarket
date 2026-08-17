"""
Database Initialization Script
Run this to set up the database with sample data for testing
"""
from app import create_app
from app.extensions import db
from app.models.user import User
from app.models.product import Product
from app.models.notification import Notification
from datetime import datetime

app = create_app()

with app.app_context():
    # Create all tables
    print("Creating database tables...")
    db.create_all()
    
    # Create admin user
    print("Creating admin user...")
    admin = User.query.filter_by(email='admin@agrimarket.com').first()
    if not admin:
        admin = User(
            name='Admin',
            email='admin@agrimarket.com',
            role='admin',
            phone='9999999999',
            is_verified=True,
            is_active=True
        )
        admin.set_password('admin123')
        db.session.add(admin)
    
    # Create sample farmer
    print("Creating sample farmer...")
    farmer = User.query.filter_by(email='farmer@test.com').first()
    if not farmer:
        farmer = User(
            name='John Farmer',
            email='farmer@test.com',
            role='farmer',
            phone='9876543210',
            address='123 Farm Road',
            city='Pune',
            state='Maharashtra',
            pincode='411001',
            is_verified=True,
            is_active=True
        )
        farmer.set_password('test123')
        db.session.add(farmer)
        db.session.flush()
        
        # Add sample products for farmer
        print("Creating sample products...")
        products = [
            {
                'name': 'Fresh Tomatoes',
                'category': 'vegetables',
                'description': 'Organic farm-fresh tomatoes',
                'price_per_unit': 50.0,
                'unit': 'kg',
                'stock_qty': 100.0,
                'min_order_qty': 5.0,
                'is_bulk_available': True,
                'bulk_price': 45.0,
                'min_bulk_qty': 50.0
            },
            {
                'name': 'Potatoes',
                'category': 'vegetables',
                'description': 'Fresh potatoes from local farm',
                'price_per_unit': 30.0,
                'unit': 'kg',
                'stock_qty': 200.0,
                'min_order_qty': 10.0,
                'is_bulk_available': True,
                'bulk_price': 25.0,
                'min_bulk_qty': 100.0
            },
            {
                'name': 'Onions',
                'category': 'vegetables',
                'description': 'Quality onions',
                'price_per_unit': 40.0,
                'unit': 'kg',
                'stock_qty': 150.0,
                'min_order_qty': 5.0,
                'is_bulk_available': False
            },
            {
                'name': 'Basmati Rice',
                'category': 'grains',
                'description': 'Premium basmati rice',
                'price_per_unit': 80.0,
                'unit': 'kg',
                'stock_qty': 500.0,
                'min_order_qty': 10.0,
                'is_bulk_available': True,
                'bulk_price': 70.0,
                'min_bulk_qty': 100.0
            },
            {
                'name': 'Fresh Mangoes',
                'category': 'fruits',
                'description': 'Sweet Alphonso mangoes',
                'price_per_unit': 150.0,
                'unit': 'kg',
                'stock_qty': 50.0,
                'min_order_qty': 2.0,
                'is_bulk_available': False
            }
        ]
        
        for product_data in products:
            product = Product(farmer_id=farmer.id, **product_data)
            db.session.add(product)
    
    # Create sample buyer
    print("Creating sample buyer...")
    buyer = User.query.filter_by(email='buyer@test.com').first()
    if not buyer:
        buyer = User(
            name='Jane Buyer',
            email='buyer@test.com',
            role='buyer',
            phone='9876543211',
            address='456 Market Street',
            city='Mumbai',
            state='Maharashtra',
            pincode='400001',
            is_verified=True,
            is_active=True
        )
        buyer.set_password('test123')
        db.session.add(buyer)
    
    # Commit all changes
    db.session.commit()
    
    print("\n" + "="*50)
    print("Database initialized successfully!")
    print("="*50)
    print("\nDefault accounts created:")
    print("\n1. Admin Account:")
    print("   Email: admin@agrimarket.com")
    print("   Password: admin123")
    print("\n2. Farmer Account:")
    print("   Email: farmer@test.com")
    print("   Password: test123")
    print("   Products: 5 sample products added")
    print("\n3. Buyer Account:")
    print("   Email: buyer@test.com")
    print("   Password: test123")
    print("\nYou can now run the application with: python run.py")
    print("="*50)
