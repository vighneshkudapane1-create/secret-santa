"""
Flask application factory
"""
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_mail import Mail
from config import config
import os

# Initialize extensions
db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.login_message = 'Please log in to access this page.'
login_manager.login_message_category = 'info'
mail = Mail()

def create_app(config_name='development'):
    """Application factory function"""
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    
    # Initialize extensions with app
    db.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)
    
    # Register blueprints
    from app.routes.auth import auth_bp
    from app.routes.dashboard import dashboard_bp
    from app.routes.events import events_bp
    from app.routes.admin import admin_bp
    from app.routes.api import api_bp
    from app.routes.wishlist import wishlist_bp
    from app.routes.gifts import gifts_bp
    from app.routes.messages import messages_bp
    from app.routes.analytics import analytics_bp
    
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(dashboard_bp, url_prefix='/dashboard')
    app.register_blueprint(events_bp, url_prefix='/events')
    app.register_blueprint(admin_bp, url_prefix='/admin')
    app.register_blueprint(api_bp, url_prefix='/api')
    app.register_blueprint(wishlist_bp, url_prefix='/wishlist')
    app.register_blueprint(gifts_bp, url_prefix='/gifts')
    app.register_blueprint(messages_bp, url_prefix='/messages')
    app.register_blueprint(analytics_bp, url_prefix='/analytics')
    
    # Root route
    @app.route('/')
    def index():
        from flask_login import current_user
        if current_user.is_authenticated:
            from flask import redirect, url_for
            return redirect(url_for('dashboard.index'))
        else:
            from flask import redirect, url_for
            return redirect(url_for('auth.login'))
    
    # Create database tables
    with app.app_context():
        db.create_all()
    
    # User loader for Flask-Login
    from app.models import User
    
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    
    # Error handlers
    @app.errorhandler(404)
    def not_found_error(error):
        return render_template('errors/404.html'), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        db.session.rollback()
        return render_template('errors/500.html'), 500
    
    return app
