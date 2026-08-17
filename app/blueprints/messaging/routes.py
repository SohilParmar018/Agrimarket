"""
Messaging Routes
Real-time messaging between users
"""
from flask import render_template, request, jsonify
from flask_login import login_required, current_user
from flask_socketio import emit, join_room
from app.blueprints.messaging import messaging_bp
from app.models.message import Message
from app.models.user import User
from app.extensions import db, socketio


@messaging_bp.route('/')
@login_required
def index():
    """Message inbox"""
    # Get unique conversations
    conversations = db.session.query(User).join(
        Message, 
        db.or_(
            db.and_(Message.sender_id == current_user.id, Message.receiver_id == User.id),
            db.and_(Message.receiver_id == current_user.id, Message.sender_id == User.id)
        )
    ).distinct().all()
    
    return render_template('messaging/inbox.html', conversations=conversations)


@messaging_bp.route('/<int:user_id>')
@login_required
def conversation(user_id):
    """View conversation with user"""
    other_user = User.query.get_or_404(user_id)
    messages = Message.get_conversation(current_user.id, user_id)
    
    # Mark messages as read
    for msg in messages:
        if msg.receiver_id == current_user.id and not msg.is_read:
            msg.mark_as_read()
    db.session.commit()
    
    return render_template('messaging/conversation.html', 
                         other_user=other_user, 
                         messages=reversed(messages))


@messaging_bp.route('/send', methods=['POST'])
@login_required
def send_message():
    """Send message"""
    data = request.get_json()
    receiver_id = data.get('receiver_id')
    content = data.get('content')
    
    if not receiver_id or not content:
        return jsonify({'error': 'Invalid data'}), 400
    
    message = Message(
        sender_id=current_user.id,
        receiver_id=receiver_id,
        content=content
    )
    db.session.add(message)
    db.session.commit()
    
    # Emit via SocketIO
    socketio.emit('new_message', message.to_dict(), room=f'user_{receiver_id}')
    
    return jsonify(message.to_dict())


@socketio.on('join')
def on_join(data):
    """Join user's room for real-time updates"""
    room = f'user_{current_user.id}'
    join_room(room)
