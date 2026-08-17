"""
Order Models
Manages orders and order items
"""
from datetime import datetime
from app.extensions import db


class Order(db.Model):
    """Order model for purchase transactions"""
    
    __tablename__ = 'orders'
    
    # Primary Key
    id = db.Column(db.Integer, primary_key=True)
    
    # Foreign Keys
    buyer_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    farmer_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    
    # Order Status
    status = db.Column(db.String(20), nullable=False, default='pending', index=True)
    # Status flow: pending → confirmed → processing → shipped → delivered → cancelled
    
    # Pricing
    total_amount = db.Column(db.Float, nullable=False, default=0)
    discount_amount = db.Column(db.Float, nullable=False, default=0)
    final_amount = db.Column(db.Float, nullable=False, default=0)
    
    # Payment
    payment_status = db.Column(db.String(20), nullable=False, default='pending')
    # pending/paid/failed/refunded
    payment_id = db.Column(db.String(100), nullable=True)  # Razorpay payment ID
    
    # Order Type
    is_b2b = db.Column(db.Boolean, default=False)
    
    # Delivery
    delivery_address = db.Column(db.Text, nullable=False)
    notes = db.Column(db.Text, nullable=True)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    confirmed_at = db.Column(db.DateTime, nullable=True)
    delivered_at = db.Column(db.DateTime, nullable=True)
    
    # Relationships
    items = db.relationship('OrderItem', backref='order', lazy='dynamic',
                           cascade='all, delete-orphan')
    
    def add_item(self, product, quantity):
        """Add item to order"""
        unit_price = product.get_price_for_quantity(quantity)
        subtotal = unit_price * quantity
        
        item = OrderItem(
            order_id=self.id,
            product_id=product.id,
            quantity=quantity,
            unit_price=unit_price,
            subtotal=subtotal
        )
        db.session.add(item)
        return item
    
    def calculate_totals(self):
        """Recalculate order totals from items"""
        self.total_amount = sum(item.subtotal for item in self.items)
        self.final_amount = self.total_amount - self.discount_amount
    
    def can_cancel(self):
        """Check if order can be cancelled"""
        return self.status in ['pending', 'confirmed']
    
    def cancel(self):
        """Cancel order and restore stock"""
        if self.can_cancel():
            self.status = 'cancelled'
            # Restore stock for all items
            for item in self.items:
                item.product.add_stock(item.quantity)
            return True
        return False
    
    def confirm(self):
        """Confirm order"""
        if self.status == 'pending':
            self.status = 'confirmed'
            self.confirmed_at = datetime.utcnow()
            return True
        return False
    
    def mark_delivered(self):
        """Mark order as delivered"""
        if self.status == 'shipped':
            self.status = 'delivered'
            self.delivered_at = datetime.utcnow()
            return True
        return False
    
    def get_status_display(self):
        """Get human-readable status"""
        status_map = {
            'pending': 'Pending Confirmation',
            'confirmed': 'Confirmed',
            'processing': 'Processing',
            'shipped': 'Shipped',
            'delivered': 'Delivered',
            'cancelled': 'Cancelled'
        }
        return status_map.get(self.status, self.status.title())
    
    def __repr__(self):
        return f'<Order #{self.id} - {self.status}>'


class OrderItem(db.Model):
    """Order item model for individual products in an order"""
    
    __tablename__ = 'order_items'
    
    # Primary Key
    id = db.Column(db.Integer, primary_key=True)
    
    # Foreign Keys
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=False, index=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    
    # Item Details
    quantity = db.Column(db.Float, nullable=False)
    unit_price = db.Column(db.Float, nullable=False)
    subtotal = db.Column(db.Float, nullable=False)
    
    def __repr__(self):
        return f'<OrderItem Order#{self.order_id} Product#{self.product_id}>'
