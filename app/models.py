"""
Database models for Secret Santa Web Application
"""
from app import db
from flask_login import UserMixin
from datetime import datetime

class User(UserMixin, db.Model):
    """User model"""
    __tablename__ = 'users'
    
    user_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password = db.Column(db.String(255), nullable=False)  # Plain text password (no hashing)
    role = db.Column(db.String(20), default='user')  # user, admin, super_admin
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)
    
    # Relationships
    events_created = db.relationship('Event', backref='creator', lazy='dynamic', foreign_keys='Event.admin_id')
    participants = db.relationship('Participant', backref='user', lazy='dynamic')
    wishlists = db.relationship('Wishlist', backref='user', lazy='dynamic')
    sent_messages = db.relationship('Message', foreign_keys='Message.sender_id', backref='sender', lazy='dynamic')
    received_messages = db.relationship('Message', foreign_keys='Message.receiver_id', backref='receiver', lazy='dynamic')
    
    def get_id(self):
        """Return user ID for Flask-Login"""
        return self.user_id
    
    def set_password(self, password):
        """Set password as plain text"""
        self.password = password
    
    def check_password(self, password):
        """Check password (plain text comparison)"""
        return self.password == password
    
    def __repr__(self):
        return f'<User {self.name}>'

class Event(db.Model):
    """Event model"""
    __tablename__ = 'events'
    
    event_id = db.Column(db.Integer, primary_key=True)
    event_name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    admin_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    budget_min = db.Column(db.Float, default=0.0)
    budget_max = db.Column(db.Float, default=1000.0)
    currency = db.Column(db.String(10), default='INR')
    invite_code = db.Column(db.String(20), unique=True, nullable=False, index=True)
    status = db.Column(db.String(20), default='pending')  # pending, active, completed, cancelled
    assignment_done = db.Column(db.Boolean, default=False)
    privacy_type = db.Column(db.String(20), default='public')  # public, private
    visibility = db.Column(db.String(20), default='all')  # all, participants_only, invite_only
    allow_public_join = db.Column(db.Boolean, default=True)  # Can anyone with invite code join?
    gift_deadline = db.Column(db.DateTime)
    event_date = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    participants = db.relationship('Participant', backref='event', lazy='dynamic', cascade='all, delete-orphan')
    assignments = db.relationship('Assignment', backref='event', lazy='dynamic', cascade='all, delete-orphan')
    messages = db.relationship('Message', backref='event', lazy='dynamic', cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Event {self.event_name}>'

class Participant(db.Model):
    """Participant model"""
    __tablename__ = 'participants'
    
    participant_id = db.Column(db.Integer, primary_key=True)
    event_id = db.Column(db.Integer, db.ForeignKey('events.event_id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    wishlist_id = db.Column(db.Integer, db.ForeignKey('wishlists.wishlist_id'), nullable=True)
    joined_at = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(20), default='active')  # active, dropped, completed
    
    # Relationships
    wishlist = db.relationship('Wishlist', backref='participant', uselist=False)
    assignments_as_giver = db.relationship('Assignment', foreign_keys='Assignment.giver_id', backref='giver', lazy='dynamic')
    assignments_as_receiver = db.relationship('Assignment', foreign_keys='Assignment.receiver_id', backref='receiver', lazy='dynamic')
    
    __table_args__ = (db.UniqueConstraint('event_id', 'user_id', name='unique_participant'),)
    
    def __repr__(self):
        return f'<Participant {self.participant_id}>'

class Wishlist(db.Model):
    """Wishlist model"""
    __tablename__ = 'wishlists'
    
    wishlist_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    event_id = db.Column(db.Integer, db.ForeignKey('events.event_id'), nullable=False)
    preferences = db.Column(db.Text)  # JSON string of preferences
    dislikes = db.Column(db.Text)  # JSON string of dislikes
    gift_category = db.Column(db.String(100))
    clothing_size = db.Column(db.String(20))
    color_preference = db.Column(db.String(50))
    hobby_tags = db.Column(db.String(200))
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<Wishlist {self.wishlist_id}>'

class Assignment(db.Model):
    """Assignment model"""
    __tablename__ = 'assignments'
    
    assignment_id = db.Column(db.Integer, primary_key=True)
    event_id = db.Column(db.Integer, db.ForeignKey('events.event_id'), nullable=False)
    giver_id = db.Column(db.Integer, db.ForeignKey('participants.participant_id'), nullable=False)
    receiver_id = db.Column(db.Integer, db.ForeignKey('participants.participant_id'), nullable=False)
    compatibility_score = db.Column(db.Float, default=0.0)
    assigned_at = db.Column(db.DateTime, default=datetime.utcnow)
    gift_status = db.Column(db.String(20), default='pending')  # pending, purchased, delivered
    
    __table_args__ = (db.UniqueConstraint('event_id', 'giver_id', name='unique_giver'),)
    
    def __repr__(self):
        return f'<Assignment {self.assignment_id}>'

class Message(db.Model):
    """Anonymous message model"""
    __tablename__ = 'messages'
    
    message_id = db.Column(db.Integer, primary_key=True)
    event_id = db.Column(db.Integer, db.ForeignKey('events.event_id'), nullable=False)
    sender_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    receiver_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    message_text = db.Column(db.Text, nullable=False)
    is_encrypted = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_read = db.Column(db.Boolean, default=False)
    
    def __repr__(self):
        return f'<Message {self.message_id}>'
