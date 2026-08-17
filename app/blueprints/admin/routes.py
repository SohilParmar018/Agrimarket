"""
Admin Routes
Platform management and statistics
"""
from flask import render_template, redirect, url_for, flash, request
from flask_login import login_required
from sqlalchemy import func
from app.blueprints.admin import admin_bp
from app.models.user import User
from app.models.product import Product
from app.models.order import Order
from app.models.notification import Notification
from app.extensions import db
from app.utils.decorators import admin_required


@admin_bp.route('/dashboard')
@login_required
@admin_required
def dashboard():
    """Admin dashboard"""
    total_users = User.query.count()
    total_farmers = User.query.filter_by(role='farmer').count()
    total_buyers = User.query.filter_by(role='buyer').count()
    total_products = Product.query.count()
    total_orders = Order.query.count()
    total_revenue = db.session.query(func.sum(Order.final_amount)).filter_by(status='delivered').scalar() or 0
    
    pending_farmers = User.query.filter_by(role='farmer', is_verified=False).count()
    
    return render_template('admin/dashboard.html',
                         total_users=total_users,
                         total_farmers=total_farmers,
                         total_buyers=total_buyers,
                         total_products=total_products,
                         total_orders=total_orders,
                         total_revenue=total_revenue,
                         pending_farmers=pending_farmers)


@admin_bp.route('/users')
@login_required
@admin_required
def users():
    """User management"""
    page = request.args.get('page', 1, type=int)
    role = request.args.get('role', 'all')
    
    query = User.query
    if role != 'all':
        query = query.filter_by(role=role)
    
    users = query.order_by(User.created_at.desc()).paginate(
        page=page, per_page=20, error_out=False
    )
    
    return render_template('admin/users.html', users=users, current_role=role)


@admin_bp.route('/users/<int:id>/verify', methods=['POST'])
@login_required
@admin_required
def verify_user(id):
    """Verify farmer account"""
    user = User.query.get_or_404(id)
    user.is_verified = True
    db.session.commit()
    
    # Notify farmer
    Notification.create_notification(
        user_id=user.id,
        type='system',
        title='Account Verified',
        message='Your farmer account has been verified by admin',
        action_url=url_for('farmer.dashboard')
    )
    
    flash(f'User {user.name} verified!', 'success')
    return redirect(url_for('admin.users'))


@admin_bp.route('/users/<int:id>/toggle-active', methods=['POST'])
@login_required
@admin_required
def toggle_user_active(id):
    """Toggle user active status"""
    user = User.query.get_or_404(id)
    user.is_active = not user.is_active
    db.session.commit()
    
    status = 'activated' if user.is_active else 'deactivated'
    flash(f'User {user.name} {status}!', 'success')
    return redirect(url_for('admin.users'))


@admin_bp.route('/orders')
@login_required
@admin_required
def orders():
    """View all orders"""
    page = request.args.get('page', 1, type=int)
    status = request.args.get('status', 'all')
    
    query = Order.query
    if status != 'all':
        query = query.filter_by(status=status)
    
    orders = query.order_by(Order.created_at.desc()).paginate(
        page=page, per_page=20, error_out=False
    )
    
    return render_template('admin/orders.html', orders=orders, current_status=status)


@admin_bp.route('/products')
@login_required
@admin_required
def products():
    """View all products"""
    page = request.args.get('page', 1, type=int)
    products = Product.query.order_by(Product.created_at.desc()).paginate(
        page=page, per_page=20, error_out=False
    )
    
    return render_template('admin/products.html', products=products)


@admin_bp.route('/broadcast', methods=['GET', 'POST'])
@login_required
@admin_required
def broadcast():
    """Broadcast notification to all users"""
    if request.method == 'POST':
        title = request.form.get('title')
        message = request.form.get('message')
        
        users = User.query.filter_by(is_active=True).all()
        for user in users:
            Notification.create_notification(
                user_id=user.id,
                type='system',
                title=title,
                message=message
            )
        
        flash(f'Notification sent to {len(users)} users!', 'success')
        return redirect(url_for('admin.dashboard'))
    
    return render_template('admin/broadcast.html')
