"""
Notification Model
Manages real-time notifications for users
"""
from datetime import datetime
from app.extensions import db


class Notification(db.Model):
    """Notification model for user alerts"""
    
    __tablename__ = 'notifications'
    
    # Primary Key
    id = db.Column(db.Integer, primary_key=True)
    
    # Foreign Key
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    
    # Notification Details
    type = db.Column(db.String(50), nullable=False, index=True)
    # Types: order/message/payment/stock/system
    
    title = db.Column(db.String(200), nullable=False)
    message = db.Column(db.Text, nullable=False)
    
    # Status
    is_read = db.Column(db.Boolean, default=False, index=True)
    
    # Action
    action_url = db.Column(db.String(255), nullable=True)
    
    # Timestamp
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False, index=True)
    
    def mark_as_read(self):
        """Mark notification as read"""
        self.is_read = True
    
    def to_dict(self):
        """Convert notification to dictionary for JSON serialization"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'type': self.type,
            'title': self.title,
            'message': self.message,
            'is_read': self.is_read,
            'action_url': self.action_url,
            'created_at': self.created_at.isoformat()
        }
    
    @staticmethod
    def create_notification(user_id, type, title, message, action_url=None):
        """Create and save a new notification"""
        notification = Notification(
            user_id=user_id,
            type=type,
            title=title,
            message=message,
            action_url=action_url
        )
        db.session.add(notification)
        db.session.commit()
        return notification
    
    @staticmethod
    def get_unread_count(user_id):
        """Get count of unread notifications for a user"""
        return Notification.query.filter_by(
            user_id=user_id,
            is_read=False
        ).count()
    
    @staticmethod
    def mark_all_read(user_id):
        """Mark all notifications as read for a user"""
        Notification.query.filter_by(
            user_id=user_id,
            is_read=False
        ).update({'is_read': True})
        db.session.commit()
    
    def __repr__(self):
        return f'<Notification {self.type} for User#{self.user_id}>'
