"""
Farmer Routes
Dashboard, inventory management, and analytics
"""
import os
from flask import render_template, redirect, url_for, flash, request, current_app, jsonify, abort
from flask_login import login_required, current_user
from sqlalchemy import func
from datetime import datetime, timedelta
from werkzeug.utils import secure_filename
from app.blueprints.farmer import farmer_bp
from app.blueprints.farmer.forms import ProductForm
from app.models.product import Product
from app.models.order import Order, OrderItem
from app.models.notification import Notification
from app.extensions import db
from app.utils.decorators import farmer_required
from app.utils.helpers import save_uploaded_file


@farmer_bp.route('/dashboard')
@login_required
@farmer_required
def dashboard():
    """Farmer dashboard"""
    # Get statistics
    total_products = Product.query.filter_by(farmer_id=current_user.id).count()
    active_orders = Order.query.filter_by(
        farmer_id=current_user.id,
        status='confirmed'
    ).count()
    
    # Today's revenue
    today = datetime.utcnow().date()
    today_orders = Order.query.filter(
        Order.farmer_id == current_user.id,
        Order.status == 'delivered',
        func.date(Order.delivered_at) == today
    ).all()
    revenue_today = sum(order.final_amount for order in today_orders)
    
    # Low stock products
    low_stock = Product.query.filter(
        Product.farmer_id == current_user.id,
        Product.stock_qty <= current_app.config.get('LOW_STOCK_THRESHOLD', 10)
    ).count()
    
    # Recent orders
    recent_orders = Order.query.filter_by(
        farmer_id=current_user.id
    ).order_by(Order.created_at.desc()).limit(5).all()
    
    return render_template('farmer/dashboard.html',
                         total_products=total_products,
                         active_orders=active_orders,
                         revenue_today=revenue_today,
                         low_stock=low_stock,
                         recent_orders=recent_orders)


@farmer_bp.route('/products')
@login_required
@farmer_required
def products():
    """List all products"""
    page = request.args.get('page', 1, type=int)
    products = Product.query.filter_by(
        farmer_id=current_user.id
    ).order_by(Product.created_at.desc()).paginate(
        page=page, per_page=10, error_out=False
    )
    return render_template('farmer/products.html', products=products)


@farmer_bp.route('/products/add', methods=['GET', 'POST'])
@login_required
@farmer_required
def add_product():
    """Add new product"""
    form = ProductForm()
    
    if form.validate_on_submit():
        product = Product(
            farmer_id=current_user.id,
            name=form.name.data,
            category=form.category.data,
            description=form.description.data,
            price_per_unit=form.price_per_unit.data,
            unit=form.unit.data,
            stock_qty=form.stock_qty.data,
            min_order_qty=form.min_order_qty.data,
            is_bulk_available=form.is_bulk_available.data,
            bulk_price=form.bulk_price.data,
            min_bulk_qty=form.min_bulk_qty.data,
            is_active=form.is_active.data
        )
        
        # Handle image upload
        if form.image.data:
            upload_folder = os.path.join(current_app.config['UPLOAD_FOLDER'], 'products')
            os.makedirs(upload_folder, exist_ok=True)
            image_path = save_uploaded_file(form.image.data, upload_folder, current_user.id)
            product.image_url = image_path
        
        db.session.add(product)
        db.session.commit()
        
        flash('Product added successfully!', 'success')
        return redirect(url_for('farmer.products'))
    
    return render_template('farmer/add_product.html', form=form)


@farmer_bp.route('/products/<int:id>/edit', methods=['GET', 'POST'])
@login_required
@farmer_required
def edit_product(id):
    """Edit product"""
    product = Product.query.get_or_404(id)
    
    if product.farmer_id != current_user.id:
        abort(403)
    
    form = ProductForm(obj=product)
    
    if form.validate_on_submit():
        product.name = form.name.data
        product.category = form.category.data
        product.description = form.description.data
        product.price_per_unit = form.price_per_unit.data
        product.unit = form.unit.data
        product.stock_qty = form.stock_qty.data
        product.min_order_qty = form.min_order_qty.data
        product.is_bulk_available = form.is_bulk_available.data
        product.bulk_price = form.bulk_price.data
        product.min_bulk_qty = form.min_bulk_qty.data
        product.is_active = form.is_active.data
        
        if form.image.data:
            upload_folder = os.path.join(current_app.config['UPLOAD_FOLDER'], 'products')
            image_path = save_uploaded_file(form.image.data, upload_folder, current_user.id)
            product.image_url = image_path
        
        db.session.commit()
        flash('Product updated successfully!', 'success')
        return redirect(url_for('farmer.products'))
    
    return render_template('farmer/edit_product.html', form=form, product=product)


@farmer_bp.route('/products/<int:id>/delete', methods=['POST'])
@login_required
@farmer_required
def delete_product(id):
    """Delete product"""
    product = Product.query.get_or_404(id)
    
    if product.farmer_id != current_user.id:
        abort(403)
    
    db.session.delete(product)
    db.session.commit()
    
    flash('Product deleted successfully!', 'success')
    return redirect(url_for('farmer.products'))


@farmer_bp.route('/orders')
@login_required
@farmer_required
def orders():
    """View farmer orders"""
    page = request.args.get('page', 1, type=int)
    status = request.args.get('status', 'all')
    
    query = Order.query.filter_by(farmer_id=current_user.id)
    
    if status != 'all':
        query = query.filter_by(status=status)
    
    orders = query.order_by(Order.created_at.desc()).paginate(
        page=page, per_page=20, error_out=False
    )
    
    return render_template('farmer/orders.html', orders=orders, current_status=status)


@farmer_bp.route('/analytics')
@login_required
@farmer_required
def analytics():
    """Farmer analytics dashboard"""
    # Get date range from query params
    days = request.args.get('days', 30, type=int)
    start_date = datetime.utcnow() - timedelta(days=days)
    
    # Daily sales data
    daily_sales = db.session.query(
        func.date(Order.delivered_at).label('date'),
        func.sum(Order.final_amount).label('revenue'),
        func.count(Order.id).label('orders')
    ).filter(
        Order.farmer_id == current_user.id,
        Order.status == 'delivered',
        Order.delivered_at >= start_date
    ).group_by(func.date(Order.delivered_at)).all()
    
    # Prepare data for charts
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
    
    # Top products
    top_products = db.session.query(
        Product.name,
        func.sum(OrderItem.subtotal).label('revenue')
    ).join(OrderItem).join(Order).filter(
        Product.farmer_id == current_user.id,
        Order.status == 'delivered'
    ).group_by(Product.id).order_by(func.sum(OrderItem.subtotal).desc()).limit(5).all()
    
    # Prepare data for charts
    top_products_labels = [product.name for product in top_products]
    top_products_data = [float(product.revenue) if product.revenue else 0 for product in top_products]
    
    return render_template('farmer/analytics.html',
                         daily_sales=daily_sales,
                         daily_sales_labels=daily_sales_labels,
                         daily_sales_data=daily_sales_data,
                         top_products=top_products,
                         top_products_labels=top_products_labels,
                         top_products_data=top_products_data,
                         days=days)
