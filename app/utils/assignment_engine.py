"""
Smart Assignment Engine for Secret Santa
"""
from app import db
from app.models import Participant, Assignment, Wishlist
import random
import json

class SmartAssignmentEngine:
    """Intelligent assignment algorithm"""
    
    def __init__(self, event_id):
        self.event_id = event_id
        self.participants = Participant.query.filter_by(
            event_id=event_id,
            status='active'
        ).all()
    
    def generate_assignments(self):
        """Generate smart assignments"""
        if len(self.participants) < 2:
            return {'success': False, 'message': 'Need at least 2 participants'}
        
        # Get existing assignments to avoid
        existing_assignments = Assignment.query.filter_by(event_id=self.event_id).all()
        existing_pairs = {(a.giver_id, a.receiver_id) for a in existing_assignments}
        
        # Try multiple times to find valid assignment
        max_attempts = 100
        for attempt in range(max_attempts):
            assignment_map = self._create_assignment_map()
            
            if assignment_map and self._is_valid_assignment(assignment_map, existing_pairs):
                # Save assignments
                for giver_id, receiver_id in assignment_map.items():
                    assignment = Assignment(
                        event_id=self.event_id,
                        giver_id=giver_id,
                        receiver_id=receiver_id,
                        compatibility_score=self._calculate_compatibility(giver_id, receiver_id)
                    )
                    db.session.add(assignment)
                
                return {'success': True, 'message': 'Assignments generated successfully'}
        
        return {'success': False, 'message': 'Could not generate valid assignments after multiple attempts'}
    
    def _create_assignment_map(self):
        """Create random assignment map"""
        participant_ids = [p.participant_id for p in self.participants]
        receiver_ids = participant_ids.copy()
        random.shuffle(receiver_ids)
        
        assignment_map = {}
        for i, giver_id in enumerate(participant_ids):
            receiver_id = receiver_ids[i]
            assignment_map[giver_id] = receiver_id
        
        return assignment_map
    
    def _is_valid_assignment(self, assignment_map, existing_pairs):
        """Check if assignment is valid"""
        # No self-assignment
        for giver_id, receiver_id in assignment_map.items():
            if giver_id == receiver_id:
                return False
            
            # Avoid existing pairs
            if (giver_id, receiver_id) in existing_pairs:
                return False
        
        # Each receiver should be unique
        receivers = list(assignment_map.values())
        if len(receivers) != len(set(receivers)):
            return False
        
        return True
    
    def _calculate_compatibility(self, giver_id, receiver_id):
        """Calculate compatibility score based on wishlists"""
        giver_participant = Participant.query.get(giver_id)
        receiver_participant = Participant.query.get(receiver_id)
        
        if not giver_participant or not receiver_participant:
            return 0.0
        
        receiver_wishlist = Wishlist.query.filter_by(
            user_id=receiver_participant.user_id,
            event_id=self.event_id
        ).first()
        
        if not receiver_wishlist:
            return 0.5  # Default score if no wishlist
        
        # Simple compatibility based on preferences
        score = 0.5  # Base score
        
        # Add score based on category match, etc.
        # This is a simplified version - can be enhanced
        
        return min(score, 1.0)
