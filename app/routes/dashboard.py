"""
Dashboard routes
"""
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app import db
from app.models import User, Event, Participant, Assignment

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/')
@login_required
def index():
    """Main dashboard"""
    # Get user's events (as participant)
    user_participations = Participant.query.filter_by(
        user_id=current_user.user_id,
        status='active'
    ).all()
    
    events = [p.event for p in user_participations]
    
    # Also get events created by user (as admin)
    created_events = Event.query.filter_by(admin_id=current_user.user_id).all()
    
    # Combine and remove duplicates
    all_user_events = {}
    for event in events:
        all_user_events[event.event_id] = event
    for event in created_events:
        if event.event_id not in all_user_events:
            all_user_events[event.event_id] = event
    
    events = list(all_user_events.values())
    # Sort by created date (newest first)
    events.sort(key=lambda x: x.created_at, reverse=True)
    
    # Get assignments for user
    assignments = []
    for participation in user_participations:
        assignment = Assignment.query.filter_by(
            event_id=participation.event_id,
            giver_id=participation.participant_id
        ).first()
        if assignment:
            receiver_participant = Participant.query.get(assignment.receiver_id)
            if receiver_participant:
                assignments.append({
                    'event': participation.event,
                    'receiver': receiver_participant.user,
                    'assignment': assignment
                })
    
    return render_template('dashboard/index.html', events=events, assignments=assignments)

@dashboard_bp.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    """User profile page (view + edit basic details)"""
    if request.method == 'POST':
        name = (request.form.get('name') or '').strip()
        email = (request.form.get('email') or '').strip()

        # Basic validation
        if not name or not email:
            flash('नाव आणि ईमेल दोन्ही भरावे लागतील.', 'danger')
            return redirect(url_for('dashboard.profile'))

        # Check if email already used by another user
        existing = User.query.filter(
            User.email == email,
            User.user_id != current_user.user_id
        ).first()
        if existing:
            flash('हा ईमेल आधीच दुसऱ्या युजरने वापरला आहे.', 'danger')
            return redirect(url_for('dashboard.profile'))

        # Update current user
        current_user.name = name
        current_user.email = email
        db.session.commit()

        flash('प्रोफाइल यशस्वीरित्या अपडेट झाले.', 'success')
        return redirect(url_for('dashboard.profile'))

    return render_template('dashboard/profile.html', user=current_user)
