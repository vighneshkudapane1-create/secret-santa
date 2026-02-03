"""
Anonymous Messaging routes
"""
from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from app import db
from app.models import Event, Participant, Message, Assignment

messages_bp = Blueprint('messages', __name__)

@messages_bp.route('/event/<int:event_id>/messages')
@login_required
def view_messages(event_id):
    """View messages for an event"""
    event = Event.query.get_or_404(event_id)
    
    # Check if user is participant
    participant = Participant.query.filter_by(
        event_id=event_id,
        user_id=current_user.user_id
    ).first()
    
    if not participant:
        flash('You are not a participant in this event.', 'error')
        return redirect(url_for('events.view_event', event_id=event_id))
    
    # Get received messages (for current user)
    received_messages = Message.query.filter_by(
        event_id=event_id,
        receiver_id=current_user.user_id
    ).all()
    
    # Get sent messages (by current user)
    sent_messages = Message.query.filter_by(
        event_id=event_id,
        sender_id=current_user.user_id
    ).all()
    
    # Combine and sort all messages chronologically
    all_messages = []
    for msg in received_messages:
        all_messages.append({
            'message': msg,
            'type': 'received',
            'timestamp': msg.created_at
        })
    for msg in sent_messages:
        all_messages.append({
            'message': msg,
            'type': 'sent',
            'timestamp': msg.created_at
        })
    
    # Sort by timestamp (oldest first)
    all_messages.sort(key=lambda x: x['timestamp'])
    
    # Mark unread messages as read
    unread_count = Message.query.filter_by(
        event_id=event_id,
        receiver_id=current_user.user_id,
        is_read=False
    ).count()
    
    # Get assignment to know who to message
    assignment = None
    if participant:
        assignment = Assignment.query.filter_by(
            event_id=event_id,
            giver_id=participant.participant_id
        ).first()
    
    return render_template('messages/chat.html', 
                         event=event, 
                         all_messages=all_messages,
                         assignment=assignment,
                         unread_count=unread_count)

@messages_bp.route('/event/<int:event_id>/send', methods=['GET', 'POST'])
@login_required
def send_message(event_id):
    """Send anonymous message"""
    event = Event.query.get_or_404(event_id)
    
    # Check if user is participant
    participant = Participant.query.filter_by(
        event_id=event_id,
        user_id=current_user.user_id
    ).first()
    
    if not participant:
        flash('You are not a participant in this event.', 'error')
        return redirect(url_for('events.view_event', event_id=event_id))
    
    # Get assignment to know receiver
    assignment = Assignment.query.filter_by(
        event_id=event_id,
        giver_id=participant.participant_id
    ).first()
    
    if not assignment:
        flash('You do not have an assignment yet. Wait for admin to generate assignments.', 'error')
        return redirect(url_for('events.view_event', event_id=event_id))
    
    receiver_participant = Participant.query.get(assignment.receiver_id)
    if not receiver_participant:
        flash('Receiver not found.', 'error')
        return redirect(url_for('events.view_event', event_id=event_id))
    
    if request.method == 'POST':
        message_text = request.form.get('message_text', '').strip()
        
        if not message_text:
            flash('Message cannot be empty.', 'error')
            return redirect(url_for('messages.view_messages', event_id=event_id))
        
        if len(message_text) > 1000:
            flash('Message is too long (max 1000 characters).', 'error')
            return redirect(url_for('messages.view_messages', event_id=event_id))
        
        message = Message(
            event_id=event_id,
            sender_id=current_user.user_id,
            receiver_id=receiver_participant.user_id,
            message_text=message_text,
            is_encrypted=False,
            is_read=False
        )
        
        try:
            db.session.add(message)
            db.session.commit()
            
            # Send email notification to receiver
            try:
                from app.utils.email_service import send_new_message_email
                send_new_message_email(message, receiver_participant.user, "Anonymous", event)
            except Exception as e:
                print(f"Error sending email: {str(e)}")
            
            flash('Message sent anonymously!', 'success')
            return redirect(url_for('messages.view_messages', event_id=event_id))
        except Exception as e:
            db.session.rollback()
            flash(f'Error sending message: {str(e)}', 'error')
    
    # For GET request, redirect to chat view
    return redirect(url_for('messages.view_messages', event_id=event_id))
    
    return render_template('messages/send.html', 
                         event=event, 
                         receiver=receiver_participant.user,
                         assignment=assignment)

@messages_bp.route('/message/<int:message_id>/read', methods=['POST'])
@login_required
def mark_read(message_id):
    """Mark message as read"""
    message = Message.query.get_or_404(message_id)
    
    # Check if current user is receiver
    if message.receiver_id != current_user.user_id:
        return jsonify({'success': False, 'message': 'Permission denied'}), 403
    
    try:
        message.is_read = True
        db.session.commit()
        return jsonify({'success': True, 'message': 'Message marked as read'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 500

@messages_bp.route('/message/<int:message_id>/delete', methods=['POST'])
@login_required
def delete_message(message_id):
    """Delete message (only receiver can delete)"""
    message = Message.query.get_or_404(message_id)
    
    # Check if current user is receiver
    if message.receiver_id != current_user.user_id:
        flash('You can only delete messages you received.', 'error')
        return redirect(url_for('messages.view_messages', event_id=message.event_id))
    
    try:
        db.session.delete(message)
        db.session.commit()
        flash('Message deleted successfully.', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error deleting message: {str(e)}', 'error')
    
    return redirect(url_for('messages.view_messages', event_id=message.event_id))
