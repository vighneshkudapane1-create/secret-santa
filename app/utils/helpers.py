"""
Helper utilities
"""
import secrets
import string

def generate_invite_code(length=8):
    """Generate random invite code"""
    characters = string.ascii_uppercase + string.digits
    return ''.join(secrets.choice(characters) for _ in range(length))

def format_currency(amount, currency='INR'):
    """Format currency"""
    if currency == 'INR':
        return f'₹{amount:,.2f}'
    elif currency == 'USD':
        return f'${amount:,.2f}'
    else:
        return f'{amount:,.2f} {currency}'
