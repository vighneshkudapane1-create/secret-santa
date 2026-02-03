# 🎁 Smart Secret Santa - Intelligent Gift Exchange Web Platform

A comprehensive web application for organizing and managing Secret Santa gift exchange events with smart matching, wishlists, anonymous messaging, and analytics.

## 🚀 Features

- **Multi-Event Management**: Create and join multiple Secret Santa events
- **Smart Assignment Engine**: Intelligent matching algorithm with compatibility scoring
- **Wishlist System**: Users can add preferences and wishlists
- **Budget Control**: Set and manage budget limits per event
- **Anonymous Messaging**: Secure chat between participants
- **Notification System**: Email notifications for events
- **Admin Dashboard**: Analytics and event management
- **Responsive Design**: Works on desktop and mobile devices

## 🛠️ Technology Stack

- **Frontend**: HTML5, CSS3, Bootstrap 5, JavaScript
- **Backend**: Python 3.x, Flask
- **Database**: MySQL
- **Authentication**: Session-based with password hashing

## 📁 Project Structure

```
secrete-santa/
├── app/
│   ├── __init__.py
│   ├── models.py
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── auth.py
│   │   ├── events.py
│   │   ├── dashboard.py
│   │   ├── admin.py
│   │   └── api.py
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── assignment_engine.py
│   │   ├── validators.py
│   │   └── helpers.py
│   └── templates/
│       ├── base.html
│       ├── auth/
│       ├── dashboard/
│       ├── events/
│       └── admin/
├── static/
│   ├── css/
│   ├── js/
│   ├── images/
│   └── assets/
├── config.py
├── requirements.txt
├── .gitignore
├── run.py
└── README.md
```

## 🚦 Getting Started

### Prerequisites
- Python 3.8+
- MySQL 5.7+
- pip

### Installation

1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Configure database in `config.py`
4. Run the application:
   ```bash
   python run.py
   ```

## 📝 License

This project is created for educational purposes.
