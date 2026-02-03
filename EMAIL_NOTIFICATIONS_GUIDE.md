# 📧 Email Notifications System Guide

## ✅ What Was Implemented

### Complete Email Notification System

1. **Event Created Email** ✅
   - Sent to event creator when event is created
   - Includes event details, budget, deadlines
   - Beautiful HTML template

2. **Assignment Notification Email** ✅
   - Sent to all participants when assignments are generated
   - Reveals Secret Santa recipient
   - Includes event details and next steps

3. **New Message Email** ✅
   - Sent to receiver when new anonymous message arrives
   - Shows message preview
   - Link to view full message

4. **Deadline Reminder Email** ✅
   - Can be sent for gift deadline reminders
   - Includes deadline date and event info

5. **Event Status Email** ✅
   - Sent when event status changes (completed/cancelled)
   - Notifies all participants

6. **Participant Joined Email** ✅
   - Sent to admin when new participant joins
   - Includes participant details

---

## 🔧 Configuration

### Email Settings in `config.py`:

```python
MAIL_SERVER = 'smtp.gmail.com'  # or your SMTP server
MAIL_PORT = 587
MAIL_USE_TLS = True
MAIL_USERNAME = 'your-email@gmail.com'
MAIL_PASSWORD = 'your-app-password'
```

### For Gmail:
1. Enable 2-Factor Authentication
2. Generate App Password: https://myaccount.google.com/apppasswords
3. Use App Password in `MAIL_PASSWORD`

### For Other Email Providers:
- **Outlook**: smtp-mail.outlook.com, Port 587
- **Yahoo**: smtp.mail.yahoo.com, Port 587
- **Custom SMTP**: Use your provider's settings

---

## 📋 Email Templates

All templates are in `app/templates/emails/`:
- `event_created.html` - Event creation notification
- `assignment_notification.html` - Assignment reveal
- `new_message.html` - New message alert
- `deadline_reminder.html` - Deadline reminder
- `event_status.html` - Status change notification
- `participant_joined.html` - New participant notification

---

## 🚀 How It Works

### Automatic Email Triggers:

1. **Event Created**:
   - When user creates new event
   - Email sent to creator

2. **Assignments Generated**:
   - When admin generates assignments
   - Email sent to all participants with their assignments

3. **New Message**:
   - When anonymous message is sent
   - Email sent to receiver

4. **Event Status Changed**:
   - When event is marked completed/cancelled
   - Email sent to all participants

5. **Participant Joined**:
   - When new user joins event
   - Email sent to event admin

---

## 📧 Email Service Functions

Located in `app/utils/email_service.py`:

- `send_event_created_email()` - Event creation
- `send_assignment_email()` - Assignment notification
- `send_new_message_email()` - New message alert
- `send_deadline_reminder_email()` - Deadline reminder
- `send_event_status_email()` - Status change
- `send_participant_joined_email()` - New participant

---

## ⚙️ Setup Instructions

### Step 1: Install Dependencies
```bash
pip install Flask-Mail==0.9.1
```

### Step 2: Configure Email Settings

**Option A: Environment Variables (Recommended)**
```bash
export MAIL_SERVER=smtp.gmail.com
export MAIL_PORT=587
export MAIL_USE_TLS=true
export MAIL_USERNAME=your-email@gmail.com
export MAIL_PASSWORD=your-app-password
```

**Option B: Direct in config.py**
Edit `config.py` and set:
```python
MAIL_USERNAME = 'your-email@gmail.com'
MAIL_PASSWORD = 'your-app-password'
```

### Step 3: Test Email Sending

Create a test script:
```python
from app import create_app
from app.utils.email_service import send_event_created_email
from app.models import Event, User

app = create_app()
with app.app_context():
    # Test email
    event = Event.query.first()
    user = User.query.first()
    if event and user:
        send_event_created_email(event, user)
        print("Test email sent!")
```

---

## 🎨 Email Template Features

- ✅ Beautiful HTML design
- ✅ Responsive layout
- ✅ Gradient headers
- ✅ Action buttons
- ✅ Event details
- ✅ Professional styling

---

## 🔒 Security Notes

- ✅ Emails sent asynchronously (non-blocking)
- ✅ Error handling for failed sends
- ✅ No sensitive data in emails
- ✅ Anonymous messaging preserved

---

## 📊 Email Status

- **Sent**: Email queued and sent
- **Failed**: Error logged (check console)
- **Async**: Non-blocking (doesn't slow down app)

---

## 🐛 Troubleshooting

### Emails Not Sending?

1. **Check Configuration**:
   - Verify MAIL_USERNAME and MAIL_PASSWORD
   - Check SMTP server settings

2. **Gmail Issues**:
   - Enable "Less secure app access" OR
   - Use App Password (recommended)

3. **Check Console**:
   - Look for error messages
   - Check email service logs

4. **Test Connection**:
   ```python
   from flask_mail import Message
   from app import mail
   
   msg = Message('Test', recipients=['your-email@gmail.com'])
   msg.body = 'Test email'
   mail.send(msg)
   ```

---

## ✅ Testing Checklist

- [ ] Event created email sent
- [ ] Assignment emails sent to all participants
- [ ] New message email sent to receiver
- [ ] Event status email sent on status change
- [ ] Participant joined email sent to admin
- [ ] All emails have correct content
- [ ] Email links work correctly

---

## 🎯 Next Steps

1. **Configure Email Settings** - Set up SMTP
2. **Test Email Sending** - Verify it works
3. **Customize Templates** - Add your branding
4. **Set Up Reminders** - Schedule deadline reminders

---

**Email Notifications System Ready! 📧✨**
