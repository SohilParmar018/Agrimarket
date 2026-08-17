"""
B2B Contract Model
Manages bulk orders and wholesale contracts
"""
from datetime import datetime
from app.extensions import db


class B2BContract(db.Model):
    """B2B Contract model for bulk/wholesale orders"""
    
    __tablename__ = 'b2b_contracts'
    
    # Primary Key
    id = db.Column(db.Integer, primary_key=True)
    
    # Foreign Keys
    buyer_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    farmer_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    
    # Contract Terms
    agreed_price_per_unit = db.Column(db.Float, nullable=False)
    total_volume = db.Column(db.Float, nullable=False)
    unit = db.Column(db.String(20), nullable=False, default='kg')
    
    # Payment
    advance_paid = db.Column(db.Float, nullable=False, default=0)
    remaining_amount = db.Column(db.Float, nullable=False, default=0)
    
    # Schedule
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    delivery_schedule = db.Column(db.Text, nullable=True)  # JSON or text description
    
    # Status
    status = db.Column(db.String(20), nullable=False, default='draft', index=True)
    # Status: draft/active/completed/cancelled
    
    # Documents
    terms_pdf_url = db.Column(db.String(255), nullable=True)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def calculate_total_amount(self):
        """Calculate total contract amount"""
        return self.agreed_price_per_unit * self.total_volume
    
    def calculate_remaining_amount(self):
        """Calculate remaining payment amount"""
        total = self.calculate_total_amount()
        self.remaining_amount = total - self.advance_paid
        return self.remaining_amount
    
    def is_active(self):
        """Check if contract is currently active"""
        if self.status != 'active':
            return False
        today = datetime.utcnow().date()
        return self.start_date <= today <= self.end_date
    
    def can_activate(self):
        """Check if contract can be activated"""
        return self.status == 'draft' and self.advance_paid > 0
    
    def activate(self):
        """Activate the contract"""
        if self.can_activate():
            self.status = 'active'
            self.calculate_remaining_amount()
            return True
        return False
    
    def complete(self):
        """Mark contract as completed"""
        if self.status == 'active':
            self.status = 'completed'
            return True
        return False
    
    def cancel(self):
        """Cancel the contract"""
        if self.status in ['draft', 'active']:
            self.status = 'cancelled'
            return True
        return False
    
    def get_status_display(self):
        """Get human-readable status"""
        status_map = {
            'draft': 'Draft',
            'active': 'Active',
            'completed': 'Completed',
            'cancelled': 'Cancelled'
        }
        return status_map.get(self.status, self.status.title())
    
    def __repr__(self):
        return f'<B2BContract #{self.id} - {self.status}>'
