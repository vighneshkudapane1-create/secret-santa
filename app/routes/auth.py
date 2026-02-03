"""
Authentication routes
"""
from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from flask_login import login_user, logout_user, login_required, current_user
from app import db
from app.models import User
from app.utils.validators import validate_email, validate_password

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    """User registration"""
    if current_user.is_authenticated:
        return redirect(url_for('dashboard.index'))
    
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')
        confirm_password = request.form.get('confirm_password', '')
        
        # Validation
        if not name or len(name) < 3:
            flash('Name must be at least 3 characters long.', 'error')
            return render_template('auth/register.html')
        
        if not validate_email(email):
            flash('Please enter a valid email address.', 'error')
            return render_template('auth/register.html')
        
        if not validate_password(password):
            flash('Password must be at least 6 characters long.', 'error')
            return render_template('auth/register.html')
        
        if password != confirm_password:
            flash('Passwords do not match.', 'error')
            return render_template('auth/register.html')
        
        # Check if user exists
        if User.query.filter_by(email=email).first():
            flash('Email already registered. Please login instead.', 'error')
            return redirect(url_for('auth.login'))
        
        # Create new user
        user = User(name=name, email=email, password=password)
        
        try:
            db.session.add(user)
            db.session.commit()
            flash('Registration successful! Please login.', 'success')
            return redirect(url_for('auth.login'))
        except Exception as e:
            db.session.rollback()
            flash('An error occurred during registration. Please try again.', 'error')
    
    return render_template('auth/register.html')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """User login"""
    if current_user.is_authenticated:
        return redirect(url_for('dashboard.index'))
    
    if request.method == 'POST':
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')
        remember = request.form.get('remember', False)
        
        if not email or not password:
            flash('Please enter both email and password.', 'error')
            return render_template('auth/login.html')
        
        user = User.query.filter_by(email=email).first()
        
        if user and user.check_password(password):
            if not user.is_active:
                flash('Your account is deactivated. Please contact admin.', 'error')
                return render_template('auth/login.html')
            
            login_user(user, remember=remember)
            next_page = request.args.get('next')
            flash(f'Welcome back, {user.name}!', 'success')
            return redirect(next_page) if next_page else redirect(url_for('dashboard.index'))
        else:
            flash('Invalid email or password.', 'error')
    
    return render_template('auth/login.html')

@auth_bp.route('/admin-login', methods=['GET', 'POST'])
def admin_login():
    """Admin login - separate page"""
    if current_user.is_authenticated:
        return redirect(url_for('dashboard.index'))
    
    if request.method == 'POST':
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')
        remember = request.form.get('remember', False)
        
        if not email or not password:
            flash('Please enter both email and password.', 'error')
            return render_template('auth/admin_login.html')
        
        user = User.query.filter_by(email=email).first()
        
        # Check if user exists, password matches, and is admin
        if user and user.password == password:
            if not user.is_active:
                flash('Your account is deactivated. Please contact admin.', 'error')
                return render_template('auth/admin_login.html')
            
            # Check if user is admin or super_admin
            if user.role not in ['admin', 'super_admin']:
                flash('Access denied. Admin credentials required.', 'error')
                return render_template('auth/admin_login.html')
            
            login_user(user, remember=remember)
            next_page = request.args.get('next')
            flash(f'Welcome, Admin {user.name}!', 'success')
            return redirect(next_page) if next_page else redirect(url_for('dashboard.index'))
        else:
            flash('Invalid email or password.', 'error')
    
    return render_template('auth/admin_login.html')

@auth_bp.route('/logout')
@login_required
def logout():
    """User logout"""
    logout_user()
    flash('You have been logged out successfully.', 'info')
    return redirect(url_for('auth.login'))
