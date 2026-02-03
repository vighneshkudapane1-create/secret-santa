"""
Event routes
"""
from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from app import db
from app.models import Event, Participant, Wishlist, Assignment
from app.utils.helpers import generate_invite_code
from datetime import datetime
import secrets

events_bp = Blueprint('events', __name__)

@events_bp.route('/')
@login_required
def list_events():
    """List all events (respecting privacy)"""
    # Get all events user can see
    all_events = Event.query.order_by(Event.created_at.desc()).all()
    
    # Filter based on privacy settings
    visible_events = []
    for event in all_events:
        # Admin can see all their events
        if event.admin_id == current_user.user_id:
            visible_events.append(event)
        # Check if user is participant
        elif Participant.query.filter_by(event_id=event.event_id, user_id=current_user.user_id).first():
            visible_events.append(event)
        # Public events visible to all
        elif event.privacy_type == 'public' and event.visibility == 'all':
            visible_events.append(event)
        # Private events only visible to participants
        elif event.privacy_type == 'private' and event.visibility == 'participants_only':
            # Already checked above
            pass
    
    return render_template('events/list.html', events=visible_events)

@events_bp.route('/create', methods=['GET', 'POST'])
@login_required
def create_event():
    """Create new event"""
    if request.method == 'POST':
        event_name = request.form.get('event_name', '').strip()
        description = request.form.get('description', '').strip()
        budget_min = float(request.form.get('budget_min', 0) or 0)
        budget_max = float(request.form.get('budget_max', 1000) or 1000)
        currency = request.form.get('currency', 'INR')
        gift_deadline = request.form.get('gift_deadline')
        event_date = request.form.get('event_date')
        privacy_type = request.form.get('privacy_type', 'public')
        visibility = request.form.get('visibility', 'all')
        allow_public_join = request.form.get('allow_public_join') == 'on'
        
        if not event_name:
            flash('Event name is required.', 'error')
            return render_template('events/create.html')
        
        # Generate unique invite code
        invite_code = generate_invite_code()
        while Event.query.filter_by(invite_code=invite_code).first():
            invite_code = generate_invite_code()
        
        # Parse datetime fields safely
        gift_deadline_parsed = None
        event_date_parsed = None
        
        if gift_deadline:
            try:
                # Handle datetime-local format (YYYY-MM-DDTHH:MM)
                gift_deadline_parsed = datetime.strptime(gift_deadline, '%Y-%m-%dT%H:%M')
            except ValueError:
                try:
                    gift_deadline_parsed = datetime.fromisoformat(gift_deadline.replace('Z', '+00:00'))
                except:
                    flash('Invalid gift deadline format.', 'error')
                    return render_template('events/create.html')
        
        if event_date:
            try:
                # Handle datetime-local format (YYYY-MM-DDTHH:MM)
                event_date_parsed = datetime.strptime(event_date, '%Y-%m-%dT%H:%M')
            except ValueError:
                try:
                    event_date_parsed = datetime.fromisoformat(event_date.replace('Z', '+00:00'))
                except:
                    flash('Invalid event date format.', 'error')
                    return render_template('events/create.html')
        
        event = Event(
            event_name=event_name,
            description=description,
            admin_id=current_user.user_id,
            budget_min=budget_min,
            budget_max=budget_max,
            currency=currency,
            invite_code=invite_code,
            gift_deadline=gift_deadline_parsed,
            event_date=event_date_parsed,
            privacy_type=privacy_type,
            visibility=visibility,
            allow_public_join=allow_public_join
        )
        
        try:
            db.session.add(event)
            db.session.flush()  # Get event_id without committing
            
            # Add creator as first participant
            participant = Participant(
                event_id=event.event_id,
                user_id=current_user.user_id
            )
            db.session.add(participant)
            db.session.commit()
            
            # Send email notification
            try:
                from app.utils.email_service import send_event_created_email
                send_event_created_email(event, current_user)
            except Exception as e:
                print(f"Error sending email: {str(e)}")
            
            flash(f'Event "{event_name}" created successfully!', 'success')
            return redirect(url_for('events.view_event', event_id=event.event_id))
        except Exception as e:
            db.session.rollback()
            import traceback
            error_msg = str(e)
            print(f"Event creation error: {error_msg}")
            print(traceback.format_exc())
            flash(f'An error occurred while creating the event: {error_msg}', 'error')
    
    return render_template('events/create.html')

@events_bp.route('/<int:event_id>')
@login_required
def view_event(event_id):
    """View event details (with privacy check)"""
    event = Event.query.get_or_404(event_id)
    
    # Check access permissions
    is_admin = event.admin_id == current_user.user_id
    participant = Participant.query.filter_by(
        event_id=event_id,
        user_id=current_user.user_id
    ).first()
    
    # Privacy check
    has_access = False
    if is_admin:
        has_access = True
    elif participant:
        has_access = True
    elif event.privacy_type == 'public' and event.visibility == 'all':
        has_access = True
    elif event.privacy_type == 'private' and event.visibility == 'participants_only':
        has_access = False  # Only participants can see
    
    if not has_access:
        flash('You do not have permission to view this event.', 'error')
        return redirect(url_for('events.list_events'))
    
    participants = Participant.query.filter_by(event_id=event_id, status='active').all()
    
    # Get assignment if exists
    assignment = None
    if participant:
        assignment = Assignment.query.filter_by(
            event_id=event_id,
            giver_id=participant.participant_id
        ).first()
    
    # Get unread message count
    from app.models import Message
    unread_count = 0
    received_messages = []
    if participant:
        received_messages = Message.query.filter_by(
            event_id=event_id,
            receiver_id=current_user.user_id
        ).all()
        unread_count = Message.query.filter_by(
            event_id=event_id,
            receiver_id=current_user.user_id,
            is_read=False
        ).count()
    
    return render_template('events/view.html', 
                         event=event, 
                         participant=participant,
                         is_admin=is_admin,
                         participants=participants,
                         assignment=assignment,
                         received_messages=received_messages,
                         unread_count=unread_count)

@events_bp.route('/join', methods=['GET', 'POST'])
@login_required
def join_event():
    """Join event by invite code"""
    if request.method == 'POST':
        invite_code = request.form.get('invite_code', '').strip().upper()
        
        if not invite_code:
            flash('Please enter an invite code.', 'error')
            return render_template('events/join.html')
        
        event = Event.query.filter_by(invite_code=invite_code).first()
        
        if not event:
            flash('Invalid invite code.', 'error')
            return render_template('events/join.html')
        
        # Privacy check for joining
        if event.privacy_type == 'private' and not event.allow_public_join:
            flash('This is a private event. Only invited participants can join.', 'error')
            return render_template('events/join.html')
        
        if event.status != 'pending' and event.status != 'active':
            flash('This event is no longer accepting participants.', 'error')
            return render_template('events/join.html')
        
        # Check if already a participant
        existing = Participant.query.filter_by(
            event_id=event.event_id,
            user_id=current_user.user_id
        ).first()
        
        if existing:
            flash('You are already a participant in this event.', 'info')
            return redirect(url_for('events.view_event', event_id=event.event_id))
        
        participant = Participant(
            event_id=event.event_id,
            user_id=current_user.user_id
        )
        
        try:
            db.session.add(participant)
            db.session.commit()
            
            # Send email notification to admin
            try:
                from app.utils.email_service import send_participant_joined_email
                admin = event.creator
                send_participant_joined_email(event, participant, admin)
            except Exception as e:
                print(f"Error sending email: {str(e)}")
            
            flash(f'Successfully joined "{event.event_name}"!', 'success')
            return redirect(url_for('events.view_event', event_id=event.event_id))
        except Exception as e:
            db.session.rollback()
            flash('An error occurred while joining the event.', 'error')
    
    return render_template('events/join.html')

@events_bp.route('/<int:event_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_event(event_id):
    """Edit event (only creator or super_admin)"""
    event = Event.query.get_or_404(event_id)
    
    # Security check: Only creator or super_admin can edit
    if event.admin_id != current_user.user_id and current_user.role != 'super_admin':
        flash('You do not have permission to edit this event.', 'error')
        return redirect(url_for('events.view_event', event_id=event_id))
    
    if request.method == 'POST':
        # जुने time values नोंद करून ठेवा (नंतर बदल झालाय का ते पाहण्यासाठी)
        old_gift_deadline = event.gift_deadline
        old_event_date = event.event_date
        event_name = request.form.get('event_name', '').strip()
        description = request.form.get('description', '').strip()
        budget_min = float(request.form.get('budget_min', 0) or 0)
        budget_max = float(request.form.get('budget_max', 1000) or 1000)
        currency = request.form.get('currency', 'INR')
        gift_deadline = request.form.get('gift_deadline')
        event_date = request.form.get('event_date')
        privacy_type = request.form.get('privacy_type', 'public')
        visibility = request.form.get('visibility', 'all')
        allow_public_join = request.form.get('allow_public_join') == 'on'
        
        if not event_name:
            flash('Event name is required.', 'error')
            return render_template('events/edit.html', event=event)
        
        # Parse datetime fields
        gift_deadline_parsed = None
        event_date_parsed = None
        
        if gift_deadline:
            try:
                gift_deadline_parsed = datetime.strptime(gift_deadline, '%Y-%m-%dT%H:%M')
            except ValueError:
                try:
                    gift_deadline_parsed = datetime.fromisoformat(gift_deadline.replace('Z', '+00:00'))
                except:
                    flash('Invalid gift deadline format.', 'error')
                    return render_template('events/edit.html', event=event)
        
        if event_date:
            try:
                event_date_parsed = datetime.strptime(event_date, '%Y-%m-%dT%H:%M')
            except ValueError:
                try:
                    event_date_parsed = datetime.fromisoformat(event_date.replace('Z', '+00:00'))
                except:
                    flash('Invalid event date format.', 'error')
                    return render_template('events/edit.html', event=event)
        
        # Update event
        event.event_name = event_name
        event.description = description
        event.budget_min = budget_min
        event.budget_max = budget_max
        event.currency = currency
        event.gift_deadline = gift_deadline_parsed
        event.event_date = event_date_parsed
        event.privacy_type = privacy_type
        event.visibility = visibility
        event.allow_public_join = allow_public_join

        # फक्त time बदलल्यावरच notification पाठवू
        time_changed = (
            gift_deadline_parsed != old_gift_deadline or
            event_date_parsed != old_event_date
        )

        try:
            db.session.commit()

            # फक्त time बदलल्यासच सर्वांना ईमेल
            if time_changed:
                try:
                    from app.utils.email_service import send_event_status_email
                    participants = Participant.query.filter_by(event_id=event_id, status='active').all()
                    for participant in participants:
                        # Status text मध्ये "rescheduled" दाखवू
                        send_event_status_email(event, participant, 'rescheduled')
                except Exception as e:
                    print(f"Error sending event update emails: {str(e)}")

            flash(f'Event "{event_name}" updated successfully!', 'success')
            return redirect(url_for('events.view_event', event_id=event_id))
        except Exception as e:
            db.session.rollback()
            flash(f'Error updating event: {str(e)}', 'error')
    
    return render_template('events/edit.html', event=event)

@events_bp.route('/<int:event_id>/delete', methods=['POST'])
@login_required
def delete_event(event_id):
    """Delete event (only creator or super_admin)"""
    event = Event.query.get_or_404(event_id)
    
    # Security check: Only creator or super_admin can delete
    if event.admin_id != current_user.user_id and current_user.role != 'super_admin':
        flash('You do not have permission to delete this event.', 'error')
        return redirect(url_for('events.view_event', event_id=event_id))
    
    event_name = event.event_name
    
    try:
        # Delete event (cascade will delete participants, assignments, etc.)
        db.session.delete(event)
        db.session.commit()
        flash(f'Event "{event_name}" deleted successfully!', 'success')
        return redirect(url_for('events.list_events'))
    except Exception as e:
        db.session.rollback()
        flash(f'Error deleting event: {str(e)}', 'error')
        return redirect(url_for('events.view_event', event_id=event_id))

@events_bp.route('/<int:event_id>/end', methods=['POST'])
@login_required
def end_event(event_id):
    """End event - change status to completed (only creator or super_admin)"""
    event = Event.query.get_or_404(event_id)
    
    # Security check: Only creator or super_admin can end event
    if event.admin_id != current_user.user_id and current_user.role != 'super_admin':
        return jsonify({'success': False, 'message': 'Permission denied'}), 403
    
    new_status = request.json.get('status', 'completed')  # completed or cancelled
    
    if new_status not in ['completed', 'cancelled']:
        return jsonify({'success': False, 'message': 'Invalid status'}), 400
    
    try:
        event.status = new_status
        db.session.commit()

        # फक्त cancel केल्यावरच participants ना ईमेल पाठवू
        if new_status == 'cancelled':
            try:
                from app.utils.email_service import send_event_status_email
                participants = Participant.query.filter_by(event_id=event_id, status='active').all()
                for participant in participants:
                    send_event_status_email(event, participant, new_status)
            except Exception as e:
                print(f"Error sending status emails: {str(e)}")

        return jsonify({
            'success': True, 
            'message': f'Event status changed to {new_status}',
            'status': new_status
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 500
