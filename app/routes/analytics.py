"""
Analytics and Statistics routes
"""
from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from app import db
from app.models import User, Event, Participant, Assignment, Wishlist, Message
from datetime import datetime, timedelta
from sqlalchemy import func

analytics_bp = Blueprint('analytics', __name__)

@analytics_bp.route('/')
@login_required
def dashboard():
    """Main analytics dashboard"""
    # Check if user is admin or super_admin
    if current_user.role not in ['admin', 'super_admin']:
        flash('You do not have permission to access analytics.', 'error')
        return redirect(url_for('dashboard.index'))
    
    # Platform-wide statistics (for super_admin)
    if current_user.role == 'super_admin':
        return platform_analytics()
    else:
        return user_analytics()

def platform_analytics():
    """Platform-wide analytics for super_admin"""
    # Total statistics
    total_users = User.query.count()
    total_events = Event.query.count()
    total_participants = Participant.query.count()
    total_assignments = Assignment.query.count()
    total_wishlists = Wishlist.query.count()
    total_messages = Message.query.count()
    
    # Active users (logged in last 30 days)
    thirty_days_ago = datetime.utcnow() - timedelta(days=30)
    active_users = User.query.filter(User.created_at >= thirty_days_ago).count()
    
    # Events by status
    events_by_status = db.session.query(
        Event.status,
        func.count(Event.event_id)
    ).group_by(Event.status).all()
    
    status_dict = {status: count for status, count in events_by_status}
    status_labels = [status or 'Unknown' for status, count in events_by_status]
    status_data = [count for status, count in events_by_status]
    
    # Events created in last 30 days
    recent_events = Event.query.filter(Event.created_at >= thirty_days_ago).count()
    
    # Assignments by gift status
    gift_status_stats = db.session.query(
        Assignment.gift_status,
        func.count(Assignment.assignment_id)
    ).group_by(Assignment.gift_status).all()
    
    gift_status_dict = {status: count for status, count in gift_status_stats}
    gift_status_labels = [status or 'Unknown' for status, count in gift_status_stats]
    gift_status_data = [count for status, count in gift_status_stats]
    
    # Events by privacy
    privacy_stats = db.session.query(
        Event.privacy_type,
        func.count(Event.event_id)
    ).group_by(Event.privacy_type).all()
    
    privacy_dict = {privacy: count for privacy, count in privacy_stats}
    privacy_labels = [privacy or 'Unknown' for privacy, count in privacy_stats]
    privacy_data = [count for privacy, count in privacy_stats]
    
    # Top event creators
    top_creators = db.session.query(
        User.name,
        func.count(Event.event_id).label('event_count')
    ).join(Event, User.user_id == Event.admin_id).group_by(User.user_id, User.name).order_by(func.count(Event.event_id).desc()).limit(5).all()
    
    # Recent events
    recent_events_list = Event.query.order_by(Event.created_at.desc()).limit(10).all()
    
    # User growth (last 7 days)
    user_growth = []
    for i in range(7):
        date = datetime.utcnow() - timedelta(days=6-i)
        count = User.query.filter(
            func.date(User.created_at) == date.date()
        ).count()
        user_growth.append({'date': date.strftime('%b %d'), 'count': count})
    
    stats = {
        'total_users': total_users,
        'total_events': total_events,
        'total_participants': total_participants,
        'total_assignments': total_assignments,
        'total_wishlists': total_wishlists,
        'total_messages': total_messages,
        'active_users': active_users,
        'recent_events': recent_events,
        'events_by_status': status_dict,
        'events_by_status_labels': status_labels,
        'events_by_status_data': status_data,
        'gift_status': gift_status_dict,
        'gift_status_labels': gift_status_labels,
        'gift_status_data': gift_status_data,
        'privacy_stats': privacy_dict,
        'privacy_labels': privacy_labels,
        'privacy_data': privacy_data,
        'top_creators': top_creators,
        'recent_events_list': recent_events_list,
        'user_growth': user_growth
    }
    
    return render_template('analytics/platform.html', stats=stats)

def user_analytics():
    """User-specific analytics for event admins"""
    # Get events created by user
    user_events = Event.query.filter_by(admin_id=current_user.user_id).all()
    
    if not user_events:
        flash('You haven\'t created any events yet.', 'info')
        return redirect(url_for('events.create_event'))
    
    # Calculate statistics
    total_events = len(user_events)
    total_participants = Participant.query.filter(
        Participant.event_id.in_([e.event_id for e in user_events])
    ).count()
    
    total_assignments = Assignment.query.filter(
        Assignment.event_id.in_([e.event_id for e in user_events])
    ).count()
    
    total_wishlists = Wishlist.query.filter(
        Wishlist.event_id.in_([e.event_id for e in user_events])
    ).count()
    
    # Events by status
    events_by_status = {}
    for event in user_events:
        status = event.status
        events_by_status[status] = events_by_status.get(status, 0) + 1
    
    events_by_status_labels = list(events_by_status.keys())
    events_by_status_data = list(events_by_status.values())
    
    # Gift status across all events
    gift_status_stats = db.session.query(
        Assignment.gift_status,
        func.count(Assignment.assignment_id)
    ).filter(
        Assignment.event_id.in_([e.event_id for e in user_events])
    ).group_by(Assignment.gift_status).all()
    
    gift_status_dict = {status: count for status, count in gift_status_stats}
    gift_status_labels = [status or 'Unknown' for status, count in gift_status_stats]
    gift_status_data = [count for status, count in gift_status_stats]
    
    # Participation rate
    avg_participants = total_participants / total_events if total_events > 0 else 0
    
    # Assignment completion rate
    assignment_rate = (total_assignments / total_participants * 100) if total_participants > 0 else 0
    
    stats = {
        'total_events': total_events,
        'total_participants': total_participants,
        'total_assignments': total_assignments,
        'total_wishlists': total_wishlists,
        'events_by_status': events_by_status,
        'events_by_status_labels': events_by_status_labels,
        'events_by_status_data': events_by_status_data,
        'gift_status': gift_status_dict,
        'gift_status_labels': gift_status_labels,
        'gift_status_data': gift_status_data,
        'avg_participants': avg_participants,
        'assignment_rate': assignment_rate,
        'user_events': user_events
    }
    
    return render_template('analytics/user.html', stats=stats)

@analytics_bp.route('/event/<int:event_id>')
@login_required
def event_analytics(event_id):
    """Detailed analytics for a specific event"""
    event = Event.query.get_or_404(event_id)
    
    # Check permissions
    if event.admin_id != current_user.user_id and current_user.role != 'super_admin':
        flash('You do not have permission to view these analytics.', 'error')
        return redirect(url_for('events.view_event', event_id=event_id))
    
    # Event statistics
    participants = Participant.query.filter_by(event_id=event_id, status='active').all()
    assignments = Assignment.query.filter_by(event_id=event_id).all()
    wishlists = Wishlist.query.filter_by(event_id=event_id).all()
    messages = Message.query.filter_by(event_id=event_id).all()
    
    # Gift status breakdown
    gift_status_breakdown = db.session.query(
        Assignment.gift_status,
        func.count(Assignment.assignment_id)
    ).filter_by(event_id=event_id).group_by(Assignment.gift_status).all()
    
    gift_status_dict = {status: count for status, count in gift_status_breakdown}
    gift_status_labels = [status or 'Unknown' for status, count in gift_status_breakdown]
    gift_status_data = [count for status, count in gift_status_breakdown]
    
    # Participation timeline
    participation_timeline = []
    for participant in participants:
        participation_timeline.append({
            'date': participant.joined_at.strftime('%Y-%m-%d') if participant.joined_at else '',
            'name': participant.user.name
        })
    
    # Wishlist completion rate
    wishlist_rate = (len(wishlists) / len(participants) * 100) if participants else 0
    
    # Message statistics
    unread_messages = Message.query.filter_by(
        event_id=event_id,
        is_read=False
    ).count()
    
    # Assignment compatibility scores
    avg_compatibility = db.session.query(
        func.avg(Assignment.compatibility_score)
    ).filter_by(event_id=event_id).scalar() or 0
    
    # Create assignment lookup by giver_id
    assignment_by_giver = {a.giver_id: a for a in assignments}
    
    # Add assignment to each participant
    participants_with_assignments = []
    for participant in participants:
        assignment = assignment_by_giver.get(participant.participant_id)
        participants_with_assignments.append({
            'participant': participant,
            'assignment': assignment
        })
    
    stats = {
        'event': event,
        'total_participants': len(participants),
        'total_assignments': len(assignments),
        'total_wishlists': len(wishlists),
        'total_messages': len(messages),
        'unread_messages': unread_messages,
        'gift_status': gift_status_dict,
        'gift_status_labels': gift_status_labels,
        'gift_status_data': gift_status_data,
        'wishlist_rate': wishlist_rate,
        'avg_compatibility': avg_compatibility,
        'participation_timeline': participation_timeline,
        'participants': participants,
        'participants_with_assignments': participants_with_assignments,
        'assignments': assignments
    }
    
    return render_template('analytics/event.html', stats=stats)
