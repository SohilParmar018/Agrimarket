"""
Order Routes
Order management and status updates
"""
from flask import render_template, redirect, url_for, flash, abort, jsonify
from flask_login import login_required, current_user
from app.blueprints.orders import orders_bp
from app.models.order import Order
from app.models.notification import Notification
from app.extensions import db, socketio


@orders_bp.route('/<int:id>')
@login_required
def detail(id):
    """Order detail page"""
    order = Order.query.get_or_404(id)
    
    # Check access
    if order.buyer_id != current_user.id and order.farmer_id != current_user.id and not current_user.is_admin():
        abort(403)
    
    return render_template('orders/detail.html', order=order)


@orders_bp.route('/<int:id>/confirm', methods=['POST'])
@login_required
def confirm(id):
    """Confirm order (farmer only)"""
    order = Order.query.get_or_404(id)
    
    if order.farmer_id != current_user.id:
        abort(403)
    
    if order.confirm():
        db.session.commit()
        
        # Notify buyer
        Notification.create_notification(
            user_id=order.buyer_id,
            type='order',
            title='Order Confirmed',
            message=f'Your order #{order.id} has been confirmed',
            action_url=url_for('orders.detail', id=order.id)
        )
        
        flash('Order confirmed!', 'success')
    else:
        flash('Cannot confirm this order', 'danger')
    
    return redirect(url_for('orders.detail', id=id))


@orders_bp.route('/<int:id>/update-status', methods=['POST'])
@login_required
def update_status(id):
    """Update order status"""
    order = Order.query.get_or_404(id)
    
    if order.farmer_id != current_user.id and not current_user.is_admin():
        abort(403)
    
    from flask import request
    new_status = request.form.get('status')
    
    if new_status in ['processing', 'shipped', 'delivered']:
        order.status = new_status
        
        if new_status == 'delivered':
            order.mark_delivered()
        
        db.session.commit()
        
        # Notify buyer
        Notification.create_notification(
            user_id=order.buyer_id,
            type='order',
            title='Order Status Updated',
            message=f'Your order #{order.id} is now {order.get_status_display()}',
            action_url=url_for('orders.detail', id=order.id)
        )
        
        flash('Order status updated!', 'success')
    
    return redirect(url_for('orders.detail', id=id))


@orders_bp.route('/<int:id>/cancel', methods=['POST'])
@login_required
def cancel(id):
    """Cancel order"""
    order = Order.query.get_or_404(id)
    
    if order.buyer_id != current_user.id:
        abort(403)
    
    if order.cancel():
        db.session.commit()
        
        # Notify farmer
        Notification.create_notification(
            user_id=order.farmer_id,
            type='order',
            title='Order Cancelled',
            message=f'Order #{order.id} has been cancelled by buyer',
            action_url=url_for('orders.detail', id=order.id)
        )
        
        flash('Order cancelled successfully!', 'info')
    else:
        flash('Cannot cancel this order', 'danger')
    
    return redirect(url_for('orders.detail', id=id))
