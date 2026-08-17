"""
Product Model
Manages agricultural products listed by farmers
"""
from datetime import datetime
from app.extensions import db


class Product(db.Model):
    """Product model for farmer inventory"""
    
    __tablename__ = 'products'
    
    # Primary Key
    id = db.Column(db.Integer, primary_key=True)
    
    # Foreign Keys
    farmer_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    
    # Product Information
    name = db.Column(db.String(200), nullable=False)
    category = db.Column(db.String(100), nullable=False, index=True)
    description = db.Column(db.Text, nullable=True)
    
    # Pricing
    price_per_unit = db.Column(db.Float, nullable=False)
    unit = db.Column(db.String(20), nullable=False, default='kg')  # kg/quintal/ton/piece
    
    # Inventory
    stock_qty = db.Column(db.Float, nullable=False, default=0)
    min_order_qty = db.Column(db.Float, nullable=False, default=1)
    
    # Bulk/Wholesale
    is_bulk_available = db.Column(db.Boolean, default=False)
    bulk_price = db.Column(db.Float, nullable=True)
    min_bulk_qty = db.Column(db.Float, nullable=True)
    
    # Media
    image_url = db.Column(db.String(255), nullable=True)
    
    # Status
    is_active = db.Column(db.Boolean, default=True)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    order_items = db.relationship('OrderItem', backref='product', lazy='dynamic')
    b2b_contracts = db.relationship('B2BContract', backref='product', lazy='dynamic')
    
    def is_in_stock(self):
        """Check if product has stock available"""
        return self.stock_qty > 0
    
    def is_low_stock(self, threshold=10):
        """Check if stock is below threshold"""
        return self.stock_qty <= threshold
    
    def can_fulfill_order(self, quantity):
        """Check if order quantity can be fulfilled"""
        return self.stock_qty >= quantity
    
    def reduce_stock(self, quantity):
        """Reduce stock by quantity"""
        if self.can_fulfill_order(quantity):
            self.stock_qty -= quantity
            return True
        return False
    
    def add_stock(self, quantity):
        """Add stock quantity"""
        self.stock_qty += quantity
    
    def get_price_for_quantity(self, quantity):
        """Calculate price based on quantity (bulk discount)"""
        if self.is_bulk_available and self.min_bulk_qty and quantity >= self.min_bulk_qty:
            return self.bulk_price
        return self.price_per_unit
    
    def calculate_total(self, quantity):
        """Calculate total price for given quantity"""
        price = self.get_price_for_quantity(quantity)
        return price * quantity
    
    def __repr__(self):
        return f'<Product {self.name} by Farmer#{self.farmer_id}>'
