"""
User Model
Handles farmers, buyers, and admin users
"""
from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app.extensions import db


class User(UserMixin, db.Model):
    """User model for authentication and profile management"""
    
    __tablename__ = 'users'
    
    # Primary Key
    id = db.Column(db.Integer, primary_key=True)
    
    # Basic Information
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), nullable=False, default='buyer')  # farmer/buyer/admin
    
    # Contact Information
    phone = db.Column(db.String(15), nullable=True)
    address = db.Column(db.Text, nullable=True)
    city = db.Column(db.String(100), nullable=True)
    state = db.Column(db.String(100), nullable=True)
    pincode = db.Column(db.String(10), nullable=True)
    
    # Profile
    profile_image = db.Column(db.String(255), nullable=True)
    
    # Status Flags
    is_verified = db.Column(db.Boolean, default=False)
    is_active = db.Column(db.Boolean, default=True)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    products = db.relationship('Product', backref='farmer', lazy='dynamic', 
                              foreign_keys='Product.farmer_id')
    
    orders_as_buyer = db.relationship('Order', backref='buyer', lazy='dynamic',
                                     foreign_keys='Order.buyer_id')
    
    orders_as_farmer = db.relationship('Order', backref='farmer', lazy='dynamic',
                                      foreign_keys='Order.farmer_id')
    
    sent_messages = db.relationship('Message', backref='sender', lazy='dynamic',
                                   foreign_keys='Message.sender_id')
    
    received_messages = db.relationship('Message', backref='receiver', lazy='dynamic',
                                       foreign_keys='Message.receiver_id')
    
    notifications = db.relationship('Notification', backref='user', lazy='dynamic',
                                   cascade='all, delete-orphan')
    
    sales_reports = db.relationship('SalesReport', backref='farmer', lazy='dynamic',
                                   foreign_keys='SalesReport.farmer_id')
    
    b2b_contracts_as_buyer = db.relationship('B2BContract', backref='buyer', lazy='dynamic',
                                            foreign_keys='B2BContract.buyer_id')
    
    b2b_contracts_as_farmer = db.relationship('B2BContract', backref='farmer', lazy='dynamic',
                                             foreign_keys='B2BContract.farmer_id')
    
    def set_password(self, password):
        """Hash and set user password"""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """Verify password against hash"""
        return check_password_hash(self.password_hash, password)
    
    def is_farmer(self):
        """Check if user is a farmer"""
        return self.role == 'farmer'
    
    def is_buyer(self):
        """Check if user is a buyer"""
        return self.role == 'buyer'
    
    def is_admin(self):
        """Check if user is an admin"""
        return self.role == 'admin'
    
    def get_full_address(self):
        """Return formatted full address"""
        parts = [self.address, self.city, self.state, self.pincode]
        return ', '.join(filter(None, parts))
    
    def __repr__(self):
        return f'<User {self.email} ({self.role})>'
