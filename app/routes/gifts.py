"""
Gift status routes
"""
from flask import Blueprint, jsonify, request
from flask_login import login_required, current_user
from app import db
from app.models import Assignment, Participant

gifts_bp = Blueprint('gifts', __name__)

@gifts_bp.route('/assignment/<int:assignment_id>/status', methods=['POST'])
@login_required
def update_gift_status(assignment_id):
    """Update gift status"""
    assignment = Assignment.query.get_or_404(assignment_id)
    
    # Check if current user is the giver
    giver_participant = Participant.query.get(assignment.giver_id)
    if not giver_participant or giver_participant.user_id != current_user.user_id:
        return jsonify({'success': False, 'message': 'Permission denied'}), 403
    
    data = request.get_json()
    new_status = data.get('status', '').strip()
    
    valid_statuses = ['pending', 'purchased', 'delivered']
    if new_status not in valid_statuses:
        return jsonify({'success': False, 'message': 'Invalid status'}), 400
    
    try:
        assignment.gift_status = new_status
        db.session.commit()
        return jsonify({
            'success': True, 
            'message': f'Gift status updated to {new_status}',
            'status': new_status
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 500
