"""
Validation utilities
"""
import re

def validate_email(email):
    """Validate email format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def validate_password(password):
    """Validate password strength"""
    if len(password) < 6:
        return False
    return True

def validate_invite_code(code):
    """Validate invite code format"""
    if len(code) < 6 or len(code) > 20:
        return False
    return code.isalnum()
