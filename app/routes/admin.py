"""
Admin routes
"""
from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from app import db
from app.models import Event, Participant, Assignment, User
from app.utils.assignment_engine import SmartAssignmentEngine

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/event/<int:event_id>')
@login_required
def event_dashboard(event_id):
    """Admin dashboard for event management"""
    event = Event.query.get_or_404(event_id)
    
    # Check if user is admin
    if event.admin_id != current_user.user_id and current_user.role != 'super_admin':
        flash('You do not have permission to access this page.', 'error')
        return redirect(url_for('dashboard.index'))
    
    participants = Participant.query.filter_by(
        event_id=event_id,
        status='active'
    ).all()
    
    assignments = Assignment.query.filter_by(event_id=event_id).all()
    
    stats = {
        'total_participants': len(participants),
        'assignments_done': len(assignments),
        'assignment_percentage': (len(assignments) / len(participants) * 100) if participants else 0
    }
    
    return render_template('admin/event_dashboard.html', 
                         event=event, 
                         participants=participants,
                         assignments=assignments,
                         stats=stats)

@admin_bp.route('/event/<int:event_id>/assign', methods=['POST'])
@login_required
def trigger_assignment(event_id):
    """Trigger smart assignment for event"""
    event = Event.query.get_or_404(event_id)
    
    # Check if user is admin
    if event.admin_id != current_user.user_id and current_user.role != 'super_admin':
        return jsonify({'success': False, 'message': 'Permission denied'}), 403
    
    if event.assignment_done:
        return jsonify({'success': False, 'message': 'Assignment already done'}), 400
    
    participants = Participant.query.filter_by(
        event_id=event_id,
        status='active'
    ).all()
    
    if len(participants) < 2:
        return jsonify({'success': False, 'message': 'Need at least 2 participants'}), 400
    
    try:
        engine = SmartAssignmentEngine(event_id)
        result = engine.generate_assignments()
        
        if result['success']:
            event.assignment_done = True
            event.status = 'active'
            db.session.commit()
            return jsonify({'success': True, 'message': 'Assignments generated successfully!'})
        else:
            return jsonify({'success': False, 'message': result.get('message', 'Assignment failed')}), 400
            
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 500

@admin_bp.route('/event/<int:event_id>/reshuffle', methods=['POST'])
@login_required
def reshuffle_assignments(event_id):
    """Reshuffle assignments for event"""
    event = Event.query.get_or_404(event_id)
    
    if event.admin_id != current_user.user_id and current_user.role != 'super_admin':
        return jsonify({'success': False, 'message': 'Permission denied'}), 403
    
    try:
        # Delete existing assignments
        Assignment.query.filter_by(event_id=event_id).delete()
        
        # Generate new assignments
        engine = SmartAssignmentEngine(event_id)
        result = engine.generate_assignments()
        
        if result['success']:
            db.session.commit()
            return jsonify({'success': True, 'message': 'Assignments reshuffled successfully!'})
        else:
            db.session.rollback()
            return jsonify({'success': False, 'message': result.get('message', 'Reshuffle failed')}), 400
            
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 500
