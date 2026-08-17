"""
Notification Routes
"""
from flask import jsonify
from flask_login import login_required, current_user
from app.blueprints.notifications import notifications_bp
from app.models.notification import Notification
from app.extensions import db


@notifications_bp.route('/')
@login_required
def index():
    """Get user notifications page"""
    notifications = Notification.query.filter_by(
        user_id=current_user.id
    ).order_by(Notification.created_at.desc()).limit(50).all()
    
    from flask import render_template
    return render_template('notifications/index.html', notifications=notifications)


@notifications_bp.route('/unread-count')
@login_required
def unread_count():
    """Get unread notification count"""
    count = Notification.get_unread_count(current_user.id)
    return jsonify({'count': count})


@notifications_bp.route('/mark-read/<int:id>', methods=['POST'])
@login_required
def mark_read(id):
    """Mark notification as read"""
    notification = Notification.query.get_or_404(id)
    
    if notification.user_id != current_user.id:
        return jsonify({'error': 'Unauthorized'}), 403
    
    notification.mark_as_read()
    db.session.commit()
    
    return jsonify({'success': True})


@notifications_bp.route('/mark-all-read', methods=['POST'])
@login_required
def mark_all_read():
    """Mark all notifications as read"""
    Notification.mark_all_read(current_user.id)
    return jsonify({'success': True})
