"""
Wishlist routes
"""
from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from app import db
from app.models import Event, Participant, Wishlist

wishlist_bp = Blueprint('wishlist', __name__)

@wishlist_bp.route('/event/<int:event_id>/wishlist', methods=['GET', 'POST'])
@login_required
def manage_wishlist(event_id):
    """Manage wishlist for an event"""
    event = Event.query.get_or_404(event_id)
    
    # Check if user is participant
    participant = Participant.query.filter_by(
        event_id=event_id,
        user_id=current_user.user_id
    ).first()
    
    if not participant:
        flash('You are not a participant in this event.', 'error')
        return redirect(url_for('events.view_event', event_id=event_id))
    
    # Get or create wishlist
    wishlist = Wishlist.query.filter_by(
        user_id=current_user.user_id,
        event_id=event_id
    ).first()
    
    if request.method == 'POST':
        preferences = request.form.get('preferences', '').strip()
        dislikes = request.form.get('dislikes', '').strip()
        gift_category = request.form.get('gift_category', '').strip()
        clothing_size = request.form.get('clothing_size', '').strip()
        color_preference = request.form.get('color_preference', '').strip()
        hobby_tags = request.form.get('hobby_tags', '').strip()
        notes = request.form.get('notes', '').strip()
        
        if wishlist:
            wishlist.preferences = preferences
            wishlist.dislikes = dislikes
            wishlist.gift_category = gift_category
            wishlist.clothing_size = clothing_size
            wishlist.color_preference = color_preference
            wishlist.hobby_tags = hobby_tags
            wishlist.notes = notes
        else:
            wishlist = Wishlist(
                user_id=current_user.user_id,
                event_id=event_id,
                preferences=preferences,
                dislikes=dislikes,
                gift_category=gift_category,
                clothing_size=clothing_size,
                color_preference=color_preference,
                hobby_tags=hobby_tags,
                notes=notes
            )
            db.session.add(wishlist)
            participant.wishlist_id = wishlist.wishlist_id
        
        try:
            db.session.commit()
            flash('Wishlist saved successfully!', 'success')
            return redirect(url_for('events.view_event', event_id=event_id))
        except Exception as e:
            db.session.rollback()
            flash(f'Error saving wishlist: {str(e)}', 'error')
    
    return render_template('wishlist/manage.html', event=event, wishlist=wishlist)

@wishlist_bp.route('/event/<int:event_id>/wishlist/view/<int:user_id>')
@login_required
def view_wishlist(event_id, user_id):
    """View someone's wishlist (for Secret Santa giver)"""
    event = Event.query.get_or_404(event_id)
    
    # Check if current user has assignment for this user
    current_participant = Participant.query.filter_by(
        event_id=event_id,
        user_id=current_user.user_id
    ).first()
    
    if not current_participant:
        flash('You are not a participant in this event.', 'error')
        return redirect(url_for('events.view_event', event_id=event_id))
    
    # Get assignment
    from app.models import Assignment
    assignment = Assignment.query.filter_by(
        event_id=event_id,
        giver_id=current_participant.participant_id
    ).first()
    
    if not assignment:
        flash('Assignment not found.', 'error')
        return redirect(url_for('events.view_event', event_id=event_id))
    
    # Get receiver's participant
    receiver_participant = Participant.query.get(assignment.receiver_id)
    if not receiver_participant or receiver_participant.user_id != user_id:
        flash('You can only view your assigned receiver\'s wishlist.', 'error')
        return redirect(url_for('events.view_event', event_id=event_id))
    
    # Get wishlist
    wishlist = Wishlist.query.filter_by(
        user_id=user_id,
        event_id=event_id
    ).first()
    
    return render_template('wishlist/view.html', 
                         event=event, 
                         wishlist=wishlist,
                         receiver=receiver_participant.user,
                         assignment=assignment)
