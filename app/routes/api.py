"""
API routes
"""
from flask import Blueprint, jsonify, request
from flask_login import login_required, current_user
from app import db
from app.models import Event, Participant, Wishlist, Message

api_bp = Blueprint('api', __name__)

@api_bp.route('/wishlist', methods=['POST'])
@login_required
def save_wishlist():
    """Save user wishlist"""
    data = request.get_json()
    event_id = data.get('event_id')
    
    if not event_id:
        return jsonify({'success': False, 'message': 'Event ID required'}), 400
    
    participant = Participant.query.filter_by(
        event_id=event_id,
        user_id=current_user.user_id
    ).first()
    
    if not participant:
        return jsonify({'success': False, 'message': 'Not a participant'}), 403
    
    wishlist = Wishlist.query.filter_by(
        user_id=current_user.user_id,
        event_id=event_id
    ).first()
    
    if wishlist:
        wishlist.preferences = data.get('preferences', '')
        wishlist.dislikes = data.get('dislikes', '')
        wishlist.gift_category = data.get('gift_category', '')
        wishlist.clothing_size = data.get('clothing_size', '')
        wishlist.color_preference = data.get('color_preference', '')
        wishlist.hobby_tags = data.get('hobby_tags', '')
        wishlist.notes = data.get('notes', '')
    else:
        wishlist = Wishlist(
            user_id=current_user.user_id,
            event_id=event_id,
            preferences=data.get('preferences', ''),
            dislikes=data.get('dislikes', ''),
            gift_category=data.get('gift_category', ''),
            clothing_size=data.get('clothing_size', ''),
            color_preference=data.get('color_preference', ''),
            hobby_tags=data.get('hobby_tags', ''),
            notes=data.get('notes', '')
        )
        db.session.add(wishlist)
        participant.wishlist_id = wishlist.wishlist_id
    
    try:
        db.session.commit()
        return jsonify({'success': True, 'message': 'Wishlist saved successfully'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 500
