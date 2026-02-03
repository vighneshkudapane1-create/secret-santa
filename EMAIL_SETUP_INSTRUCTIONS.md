# 📧 Email Notifications Setup Instructions

## ✅ Email Notifications System Implemented!

All email notification features are now ready. You just need to configure your email settings.

---

## 🔧 Quick Setup (5 Minutes)

### Step 1: Install Flask-Mail
```bash
pip install Flask-Mail==0.9.1
```

### Step 2: Configure Email Settings

**Option A: Using Environment Variables (Recommended)**

Create a `.env` file in project root:
```env
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=true
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password
```

**Option B: Direct in config.py**

Edit `config.py`:
```python
MAIL_USERNAME = 'your-email@gmail.com'
MAIL_PASSWORD = 'your-app-password'
```

---

## 📧 Gmail Setup (Most Common)

### For Gmail Users:

1. **Enable 2-Factor Authentication**
   - Go to: https://myaccount.google.com/security
   - Enable 2-Step Verification

2. **Generate App Password**
   - Go to: https://myaccount.google.com/apppasswords
   - Select "Mail" and "Other (Custom name)"
   - Enter "Secret Santa App"
   - Copy the 16-character password

3. **Use App Password in Config**
   ```python
   MAIL_PASSWORD = 'xxxx xxxx xxxx xxxx'  # Your app password
   ```

---

## 🎯 Email Notifications Included

### 1. Event Created ✅
- Sent when user creates event
- Includes event details

### 2. Assignment Notification ✅
- Sent when admin generates assignments
- Reveals Secret Santa recipient
- Sent to all participants

### 3. New Message ✅
- Sent when anonymous message received
- Shows message preview

### 4. Event Status Change ✅
- Sent when event marked completed/cancelled
- Notifies all participants

### 5. Participant Joined ✅
- Sent to admin when new participant joins

---

## 🧪 Test Email Sending

### Quick Test:
```python
# test_email.py
from app import create_app
from app.utils.email_service import send_event_created_email
from app.models import Event, User

app = create_app()
with app.app_context():
    event = Event.query.first()
    user = User.query.first()
    if event and user:
        send_event_created_email(event, user)
        print("✅ Test email sent!")
```

Run:
```bash
python test_email.py
```

---

## ⚙️ Other Email Providers

### Outlook/Hotmail:
```python
MAIL_SERVER = 'smtp-mail.outlook.com'
MAIL_PORT = 587
MAIL_USE_TLS = True
```

### Yahoo:
```python
MAIL_SERVER = 'smtp.mail.yahoo.com'
MAIL_PORT = 587
MAIL_USE_TLS = True
```

### Custom SMTP:
```python
MAIL_SERVER = 'smtp.yourdomain.com'
MAIL_PORT = 587  # or 465 for SSL
MAIL_USE_TLS = True  # or False for SSL
```

---

## ✅ Verification Checklist

- [ ] Flask-Mail installed
- [ ] Email settings configured
- [ ] Gmail App Password generated (if using Gmail)
- [ ] Test email sent successfully
- [ ] Check spam folder if emails not received

---

## 🐛 Troubleshooting

### Emails Not Sending?

1. **Check Console**: Look for error messages
2. **Verify Settings**: Double-check MAIL_USERNAME and MAIL_PASSWORD
3. **Gmail Issues**: Use App Password, not regular password
4. **Firewall**: Check if port 587 is blocked
5. **Test Connection**: Use test script above

### Common Errors:

- **"Authentication failed"**: Wrong password or need App Password
- **"Connection refused"**: Check MAIL_SERVER and MAIL_PORT
- **"Timeout"**: Check firewall/network settings

---

## 📊 Email Features

- ✅ Asynchronous sending (non-blocking)
- ✅ Beautiful HTML templates
- ✅ Responsive design
- ✅ Error handling
- ✅ Multiple notification types

---

## 🎨 Customize Email Templates

All templates in `app/templates/emails/`:
- Edit HTML/CSS to match your branding
- Add your logo
- Customize colors
- Modify content

---

**Email Notifications Ready! Configure and test! 📧✨**
