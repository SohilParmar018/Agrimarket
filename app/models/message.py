"""
Message Model
Handles real-time messaging between users
"""
from datetime import datetime
from app.extensions import db


class Message(db.Model):
    """Message model for user-to-user communication"""
    
    __tablename__ = 'messages'
    
    # Primary Key
    id = db.Column(db.Integer, primary_key=True)
    
    # Foreign Keys
    sender_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    receiver_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    
    # Message Content
    content = db.Column(db.Text, nullable=False)
    message_type = db.Column(db.String(20), default='text')  # text/image
    
    # Status
    is_read = db.Column(db.Boolean, default=False)
    
    # Timestamp
    sent_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False, index=True)
    
    def mark_as_read(self):
        """Mark message as read"""
        self.is_read = True
    
    def to_dict(self):
        """Convert message to dictionary for JSON serialization"""
        return {
            'id': self.id,
            'sender_id': self.sender_id,
            'receiver_id': self.receiver_id,
            'content': self.content,
            'message_type': self.message_type,
            'is_read': self.is_read,
            'sent_at': self.sent_at.isoformat()
        }
    
    @staticmethod
    def get_conversation(user1_id, user2_id, limit=50):
        """Get conversation between two users"""
        return Message.query.filter(
            db.or_(
                db.and_(Message.sender_id == user1_id, Message.receiver_id == user2_id),
                db.and_(Message.sender_id == user2_id, Message.receiver_id == user1_id)
            )
        ).order_by(Message.sent_at.desc()).limit(limit).all()
    
    @staticmethod
    def get_unread_count(user_id):
        """Get count of unread messages for a user"""
        return Message.query.filter_by(
            receiver_id=user_id,
            is_read=False
        ).count()
    
    def __repr__(self):
        return f'<Message from User#{self.sender_id} to User#{self.receiver_id}>'
