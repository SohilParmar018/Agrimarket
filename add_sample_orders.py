"""
Add sample orders for testing analytics
Run this to populate the database with sample order data
"""
from app import create_app
from app.extensions import db
from app.models.user import User
from app.models.product import Product
from app.models.order import Order, OrderItem
from datetime import datetime, timedelta
import random

app = create_app()

with app.app_context():
    print("Adding sample orders for analytics...")
    print("-" * 50)
    
    # Get farmer and buyer
    farmer = User.query.filter_by(email='farmer@test.com').first()
    buyer = User.query.filter_by(email='buyer@test.com').first()
    
    if not farmer or not buyer:
        print("Error: Farmer or buyer not found!")
        print("Please run init_db.py first")
        exit(1)
    
    # Get farmer's products
    products = Product.query.filter_by(farmer_id=farmer.id).all()
    
    if not products:
        print("Error: No products found!")
        exit(1)
    
    print(f"Found {len(products)} products")
    print(f"Creating orders for the last 30 days...")
    
    orders_created = 0
    
    # Create orders for the last 30 days
    for i in range(30):
        # Create 1-3 orders per day
        num_orders = random.randint(1, 3)
        
        for j in range(num_orders):
            # Random date in the last 30 days
            days_ago = 29 - i
            order_date = datetime.utcnow() - timedelta(days=days_ago)
            
            # Create order
            order = Order(
                buyer_id=buyer.id,
                farmer_id=farmer.id,
                status='delivered',
                payment_status='paid',
                delivery_address=buyer.get_full_address(),
                created_at=order_date,
                confirmed_at=order_date + timedelta(hours=1),
                delivered_at=order_date + timedelta(days=2)
            )
            
            db.session.add(order)
            db.session.flush()
            
            # Add 1-3 random products to the order
            num_items = random.randint(1, min(3, len(products)))
            selected_products = random.sample(products, num_items)
            
            for product in selected_products:
                quantity = random.uniform(product.min_order_qty, product.min_order_qty * 5)
                quantity = round(quantity, 1)
                
                order.add_item(product, quantity)
            
            # Calculate totals
            order.calculate_totals()
            
            orders_created += 1
    
    db.session.commit()
    
    print("-" * 50)
    print(f"✓ Created {orders_created} sample orders!")
    print()
    print("Now you can view analytics:")
    print("1. Login as farmer (farmer@test.com / test123)")
    print("2. Click on 'Analytics' in the navigation")
    print("3. You'll see charts with sales data!")
    print()
    print("Restart the app if needed:")
    print("  Press CTRL+C to stop")
    print("  Run: python run.py")
