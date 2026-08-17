"""
Sales Report Model
Auto-generated sales analytics and reports
"""
from datetime import datetime, date
from app.extensions import db


class SalesReport(db.Model):
    """Sales report model for farmer analytics"""
    
    __tablename__ = 'sales_reports'
    
    # Primary Key
    id = db.Column(db.Integer, primary_key=True)
    
    # Foreign Key
    farmer_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    
    # Report Period
    period_type = db.Column(db.String(20), nullable=False, index=True)
    # Types: daily/monthly/yearly
    period_date = db.Column(db.Date, nullable=False, index=True)
    
    # Sales Metrics
    total_orders = db.Column(db.Integer, nullable=False, default=0)
    total_units_sold = db.Column(db.Float, nullable=False, default=0)
    
    # Financial Metrics
    gross_revenue = db.Column(db.Float, nullable=False, default=0)
    total_cost = db.Column(db.Float, nullable=False, default=0)
    net_profit = db.Column(db.Float, nullable=False, default=0)
    profit_margin = db.Column(db.Float, nullable=False, default=0)  # Percentage
    
    # Top Product
    top_product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=True)
    
    # Timestamp
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    
    # Relationships
    top_product = db.relationship('Product', foreign_keys=[top_product_id])
    
    def calculate_profit_margin(self):
        """Calculate profit margin percentage"""
        if self.gross_revenue > 0:
            self.profit_margin = (self.net_profit / self.gross_revenue) * 100
        else:
            self.profit_margin = 0
        return self.profit_margin
    
    @staticmethod
    def generate_daily_report(farmer_id, report_date=None):
        """Generate daily sales report for a farmer"""
        from app.models.order import Order, OrderItem
        from sqlalchemy import func
        
        if report_date is None:
            report_date = date.today()
        
        # Query orders for the day
        orders = Order.query.filter(
            Order.farmer_id == farmer_id,
            Order.status == 'delivered',
            func.date(Order.delivered_at) == report_date
        ).all()
        
        if not orders:
            return None
        
        # Calculate metrics
        total_orders = len(orders)
        gross_revenue = sum(order.final_amount for order in orders)
        
        # Calculate total units sold
        order_ids = [order.id for order in orders]
        total_units = db.session.query(func.sum(OrderItem.quantity)).filter(
            OrderItem.order_id.in_(order_ids)
        ).scalar() or 0
        
        # Find top product
        top_product = db.session.query(
            OrderItem.product_id,
            func.sum(OrderItem.subtotal).label('revenue')
        ).filter(
            OrderItem.order_id.in_(order_ids)
        ).group_by(OrderItem.product_id).order_by(
            func.sum(OrderItem.subtotal).desc()
        ).first()
        
        # Create report
        report = SalesReport(
            farmer_id=farmer_id,
            period_type='daily',
            period_date=report_date,
            total_orders=total_orders,
            total_units_sold=total_units,
            gross_revenue=gross_revenue,
            net_profit=gross_revenue,  # Simplified - can add cost calculation
            top_product_id=top_product[0] if top_product else None
        )
        report.calculate_profit_margin()
        
        db.session.add(report)
        db.session.commit()
        
        return report
    
    @staticmethod
    def get_report(farmer_id, period_type, period_date):
        """Get existing report or generate new one"""
        report = SalesReport.query.filter_by(
            farmer_id=farmer_id,
            period_type=period_type,
            period_date=period_date
        ).first()
        
        if not report and period_type == 'daily':
            report = SalesReport.generate_daily_report(farmer_id, period_date)
        
        return report
    
    def __repr__(self):
        return f'<SalesReport {self.period_type} for Farmer#{self.farmer_id} on {self.period_date}>'
