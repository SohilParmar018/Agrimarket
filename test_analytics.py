"""Test analytics data generation"""
from app import create_app
from app.models.order import Order, OrderItem
from app.models.product import Product
from app.extensions import db
from sqlalchemy import func
from datetime import datetime, timedelta

app = create_app()
app.app_context().push()

# Test farmer ID (farmer@test.com)
farmer_id = 2

print("=" * 60)
print("ANALYTICS DATA TEST")
print("=" * 60)

# Get date range
days = 30
start_date = datetime.utcnow() - timedelta(days=days)

print(f"\nDate range: Last {days} days")
print(f"Start date: {start_date.date()}")
print(f"Current date: {datetime.utcnow().date()}")

# Daily sales data
print("\n" + "=" * 60)
print("DAILY SALES DATA")
print("=" * 60)

daily_sales = db.session.query(
    func.date(Order.delivered_at).label('date'),
    func.sum(Order.final_amount).label('revenue'),
    func.count(Order.id).label('orders')
).filter(
    Order.farmer_id == farmer_id,
    Order.status == 'delivered',
    Order.delivered_at >= start_date
).group_by(func.date(Order.delivered_at)).all()

if daily_sales:
    print(f"\nFound {len(daily_sales)} days with sales:")
    for sale in daily_sales[:10]:  # Show first 10
        print(f"  {sale.date}: ₹{sale.revenue:.2f} ({sale.orders} orders)")
    
    # Prepare chart data
    daily_sales_labels = []
    daily_sales_data = []
    for sale in daily_sales:
        # Convert string date to datetime object
        if isinstance(sale.date, str):
            date_obj = datetime.strptime(sale.date, '%Y-%m-%d')
            daily_sales_labels.append(date_obj.strftime('%d %b'))
        else:
            daily_sales_labels.append(sale.date.strftime('%d %b'))
        daily_sales_data.append(float(sale.revenue) if sale.revenue else 0)
    
    print(f"\nChart labels: {daily_sales_labels[:5]}...")
    print(f"Chart data: {daily_sales_data[:5]}...")
else:
    print("\n⚠️  No daily sales data found!")

# Top products
print("\n" + "=" * 60)
print("TOP PRODUCTS BY REVENUE")
print("=" * 60)

top_products = db.session.query(
    Product.name,
    func.sum(OrderItem.subtotal).label('revenue')
).join(OrderItem).join(Order).filter(
    Product.farmer_id == farmer_id,
    Order.status == 'delivered'
).group_by(Product.id).order_by(func.sum(OrderItem.subtotal).desc()).limit(5).all()

if top_products:
    print(f"\nFound {len(top_products)} top products:")
    for product in top_products:
        print(f"  {product.name}: ₹{product.revenue:.2f}")
    
    # Prepare chart data
    top_products_labels = [product.name for product in top_products]
    top_products_data = [float(product.revenue) if product.revenue else 0 for product in top_products]
    
    print(f"\nChart labels: {top_products_labels}")
    print(f"Chart data: {top_products_data}")
else:
    print("\n⚠️  No top products data found!")

# Overall stats
print("\n" + "=" * 60)
print("OVERALL STATISTICS")
print("=" * 60)

total_orders = Order.query.filter_by(farmer_id=farmer_id).count()
delivered_orders = Order.query.filter_by(farmer_id=farmer_id, status='delivered').count()
total_revenue = db.session.query(func.sum(Order.final_amount)).filter(
    Order.farmer_id == farmer_id,
    Order.status == 'delivered'
).scalar() or 0

print(f"\nTotal orders: {total_orders}")
print(f"Delivered orders: {delivered_orders}")
print(f"Total revenue: ₹{total_revenue:.2f}")

print("\n" + "=" * 60)
print("✓ Analytics test complete!")
print("=" * 60)
