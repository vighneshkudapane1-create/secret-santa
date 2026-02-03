# 📁 Secret Santa Project - Complete Folder & File Structure

## Project Root Structure

```
secrete-santa/
│
├── app/                          # Main application package
│   ├── __init__.py              # Flask app factory
│   ├── models.py                # Database models (User, Event, Participant, etc.)
│   │
│   ├── routes/                  # Route blueprints
│   │   ├── __init__.py
│   │   ├── auth.py              # Authentication routes (login, register, logout)
│   │   ├── dashboard.py         # User dashboard routes
│   │   ├── events.py            # Event management routes
│   │   ├── admin.py             # Admin panel routes
│   │   └── api.py               # API endpoints
│   │
│   ├── utils/                   # Utility functions
│   │   ├── __init__.py
│   │   ├── assignment_engine.py # Smart assignment algorithm
│   │   ├── validators.py        # Form validation functions
│   │   └── helpers.py           # Helper utilities
│   │
│   └── templates/               # Jinja2 HTML templates
│       ├── base.html            # Base template
│       │
│       ├── auth/                # Authentication templates
│       │   ├── login.html
│       │   └── register.html
│       │
│       ├── dashboard/           # Dashboard templates
│       │   ├── index.html       # Main dashboard
│       │   └── profile.html     # User profile
│       │
│       ├── events/              # Event templates
│       │   ├── list.html        # All events list
│       │   ├── create.html      # Create event form
│       │   ├── join.html        # Join event form
│       │   └── view.html        # Event details
│       │
│       └── admin/               # Admin templates
│           └── event_dashboard.html
│       │
│       └── errors/              # Error pages
│           ├── 404.html
│           └── 500.html
│
├── static/                       # Static files
│   ├── css/
│   │   └── style.css            # Custom CSS styles
│   │
│   ├── js/
│   │   └── main.js              # Custom JavaScript
│   │
│   ├── images/                   # Image assets
│   │   └── (placeholder for images)
│   │
│   └── assets/                  # Other assets
│       └── (placeholder for fonts, etc.)
│
├── config.py                     # Application configuration
├── run.py                        # Application entry point
├── requirements.txt              # Python dependencies
├── .gitignore                    # Git ignore rules
├── README.md                     # Project documentation
└── PROJECT_STRUCTURE.md          # This file
```

## Detailed File Descriptions

### Root Files

- **`run.py`**: Main entry point to start the Flask application
- **`config.py`**: Configuration settings (database, secrets, etc.)
- **`requirements.txt`**: Python package dependencies
- **`.gitignore`**: Files and folders to ignore in Git
- **`README.md`**: Project documentation and setup instructions

### App Package (`app/`)

#### Core Files
- **`__init__.py`**: Flask application factory, initializes extensions, registers blueprints
- **`models.py`**: SQLAlchemy database models:
  - `User`: User accounts
  - `Event`: Secret Santa events
  - `Participant`: Event participants
  - `Wishlist`: User wishlists
  - `Assignment`: Secret Santa assignments
  - `Message`: Anonymous messages

#### Routes (`app/routes/`)
- **`auth.py`**: Authentication routes
  - `/auth/register` - User registration
  - `/auth/login` - User login
  - `/auth/logout` - User logout

- **`dashboard.py`**: Dashboard routes
  - `/dashboard/` - Main dashboard
  - `/dashboard/profile` - User profile

- **`events.py`**: Event management routes
  - `/events/` - List all events
  - `/events/create` - Create new event
  - `/events/join` - Join event by code
  - `/events/<id>` - View event details

- **`admin.py`**: Admin routes
  - `/admin/event/<id>` - Event management dashboard
  - `/admin/event/<id>/assign` - Trigger assignment
  - `/admin/event/<id>/reshuffle` - Reshuffle assignments

- **`api.py`**: API endpoints
  - `/api/wishlist` - Save wishlist (POST)

#### Utils (`app/utils/`)
- **`assignment_engine.py`**: Smart assignment algorithm
  - `SmartAssignmentEngine` class
  - Generates valid Secret Santa pairs
  - Avoids self-assignment and duplicates
  - Calculates compatibility scores

- **`validators.py`**: Validation functions
  - Email validation
  - Password validation
  - Invite code validation

- **`helpers.py`**: Helper utilities
  - Generate invite codes
  - Format currency
  - Other utility functions

#### Templates (`app/templates/`)
- **`base.html`**: Base template with navigation, footer, flash messages
- **Auth templates**: Login and registration forms
- **Dashboard templates**: User dashboard and profile
- **Event templates**: Event listing, creation, joining, viewing
- **Admin templates**: Event management dashboard
- **Error templates**: 404 and 500 error pages

### Static Files (`static/`)

- **`css/style.css`**: Custom styling
  - Modern gradient backgrounds
  - Card animations
  - Responsive design
  - Custom scrollbar
  - Hover effects

- **`js/main.js`**: JavaScript functionality
  - Auto-dismiss alerts
  - Form validation
  - API helper functions
  - Smooth scrolling
  - Fade-in animations

## Database Schema

### Tables
1. **users**: User accounts
2. **events**: Secret Santa events
3. **participants**: Event participants
4. **wishlists**: User wishlists
5. **assignments**: Secret Santa pairings
6. **messages**: Anonymous messages

## Technology Stack

- **Backend**: Python 3.x, Flask
- **Database**: MySQL (via PyMySQL)
- **Frontend**: HTML5, CSS3, Bootstrap 5, JavaScript
- **Authentication**: Flask-Login
- **ORM**: SQLAlchemy

## Setup Instructions

1. Install dependencies: `pip install -r requirements.txt`
2. Configure database in `config.py`
3. Run application: `python run.py`
4. Access at: `http://localhost:5000`

## Features Implemented

✅ User registration and login
✅ Event creation and management
✅ Join events via invite code
✅ Smart assignment algorithm
✅ Admin dashboard
✅ Wishlist system (API ready)
✅ Responsive design
✅ Modern UI with animations

## Next Steps

- Add email notifications
- Implement anonymous messaging UI
- Add analytics dashboard
- Enhance wishlist compatibility matching
- Add gift status tracking
