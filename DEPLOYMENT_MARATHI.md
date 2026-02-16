# 🚀 Secret Santa Application - Render वर Deploy करण्याची पूर्ण मार्गदर्शिका (Marathi)

## ✅ समस्या सोडवली

मी खालील समस्या सोडवल्या आहेत:
1. ✅ `psycopg` ची जागा `psycopg2-binary` वापरली (अधिक stable)
2. ✅ `SQLAlchemy` explicitly add केले
3. ✅ PostgreSQL connection string `psycopg2` साठी update केले

## 📋 Render वर Deploy करण्याची पायरी-पायरी मार्गदर्शिका

### **पायरी 1: GitHub वर Code Push करा**

```bash
# Terminal मध्ये हे commands run करा:
cd C:\wamp64\www\secret-santa
git add .
git commit -m "Fixed deployment issues - updated requirements and config"
git push origin main
```

**टीप:** जर Git permission error येत असेल, तर:
- GitHub वर login करा
- Personal Access Token तयार करा
- किंवा repository fork करा आपल्या account मध्ये

---

### **पायरी 2: Render Dashboard मध्ये जा**

1. [render.com](https://render.com) वर जा
2. "Sign Up" किंवा "Log In" करा
3. Dashboard मध्ये जा

---

### **पायरी 3: PostgreSQL Database तयार करा**

1. Render Dashboard मध्ये **"New +"** button click करा
2. **"PostgreSQL"** select करा
3. Database details भरा:
   - **Name:** `secret-santa-db` (किंवा आपले नाव)
   - **Database:** `secret_santa_db`
   - **User:** (auto generate होईल)
   - **Region:** आपल्या जवळचा region select करा
   - **Plan:** Free (सुरुवातीसाठी)
4. **"Create Database"** click करा
5. Database ready झाल्यानंतर, **"Connections"** tab मध्ये जा
6. **"Internal Database URL"** copy करा (हे `DATABASE_URL` environment variable मध्ये वापराल)

**उदाहरण:**
```
postgresql://user:password@dpg-xxxxx-a.oregon-postgres.render.com/secret_santa_db
```

---

### **पायरी 4: Web Service तयार करा**

1. Render Dashboard मध्ये **"New +"** button click करा
2. **"Web Service"** select करा
3. **GitHub repository connect करा:**
   - "Connect account" click करा
   - GitHub वर authorize करा
   - `vighneshkudapane1-create/secret-santa` repository select करा
   - Branch: `main` select करा

4. **Service Configuration:**
   - **Name:** `secret-santa` (किंवा आपले नाव)
   - **Environment:** `Docker` (auto-detect होईल `render.yaml` मुळे)
   - **Region:** Database सारखाच region select करा
   - **Branch:** `main`
   - **Root Directory:** (रिकामे ठेवा)
   - **Plan:** Free

---

### **पायरी 5: Environment Variables सेट करा**

Web Service create करताना किंवा नंतर **"Environment"** tab मध्ये हे variables add करा:

#### **आवश्यक Variables:**

1. **SECRET_KEY**
   ```
   SECRET_KEY=your-secret-key-here-generate-random-string
   ```
   **Secret Key generate करण्यासाठी:**
   - Python terminal मध्ये:
   ```python
   import secrets
   print(secrets.token_hex(32))
   ```
   - Output copy करा आणि `SECRET_KEY` मध्ये paste करा

2. **FLASK_ENV**
   ```
   FLASK_ENV=production
   ```

3. **DATABASE_URL**
   ```
   DATABASE_URL=postgresql://user:password@host:port/dbname
   ```
   **टीप:** PostgreSQL database चा "Internal Database URL" येथे paste करा

4. **MAIL_SERVER** (Email notifications साठी)
   ```
   MAIL_SERVER=smtp.gmail.com
   ```

5. **MAIL_PORT**
   ```
   MAIL_PORT=587
   ```

6. **MAIL_USE_TLS**
   ```
   MAIL_USE_TLS=true
   ```

7. **MAIL_USERNAME** (Gmail address)
   ```
   MAIL_USERNAME=your-email@gmail.com
   ```

8. **MAIL_PASSWORD** (Gmail App Password)
   ```
   MAIL_PASSWORD=your-app-password
   ```
   **Gmail App Password तयार करण्यासाठी:**
   - Google Account → Security → 2-Step Verification (enable करा)
   - App passwords → Generate
   - "Mail" आणि "Other" select करा
   - Generated password copy करा

---

### **पायरी 6: Deploy करा**

1. सर्व environment variables add केल्यानंतर
2. **"Create Web Service"** किंवा **"Save Changes"** click करा
3. Render automatically build आणि deploy करेल
4. **"Logs"** tab मध्ये progress बघू शकता
5. Build complete झाल्यानंतर, आपले app live होईल!

---

### **पायरी 7: Database Tables तयार करा**

Deploy झाल्यानंतर:

1. Render Dashboard मध्ये आपल्या service वर click करा
2. **"Shell"** tab मध्ये जा
3. Shell open करा आणि हे commands run करा:

```bash
python create_tables.py
```

किंवा

```bash
python -c "from app import create_app, db; app = create_app('production'); app.app_context().push(); db.create_all()"
```

---

### **पायरी 8: Admin User तयार करा**

Database tables तयार झाल्यानंतर:

```bash
python create_admin_user.py
```

किंवा Shell मध्ये:

```python
from app import create_app, db
from app.models import User
app = create_app('production')
with app.app_context():
    admin = User(
        name='Admin',
        email='admin@example.com',
        password='your-password',
        role='admin'
    )
    db.session.add(admin)
    db.session.commit()
    print("Admin user created!")
```

---

## 🔍 समस्या निराकरण (Troubleshooting)

### **समस्या 1: Build Fail होतो**

**उपाय:**
- `requirements.txt` मध्ये सर्व packages आहेत का तपासा
- Logs मध्ये error message बघा
- Python version `runtime.txt` मध्ये `python-3.11.9` आहे का तपासा

### **समस्या 2: Database Connection Error**

**उपाय:**
- `DATABASE_URL` correctly set आहे का तपासा
- PostgreSQL database running आहे का तपासा
- Internal Database URL वापरा (External नाही)

### **समस्या 3: App Start होत नाही**

**उपाय:**
- सर्व environment variables set आहेत का तपासा
- `SECRET_KEY` set आहे का तपासा
- Logs मध्ये error message बघा

### **समस्या 4: Email पाठवत नाही**

**उपाय:**
- Gmail App Password वापरा (regular password नाही)
- `MAIL_USERNAME` आणि `MAIL_PASSWORD` correctly set आहेत का तपासा
- 2-Step Verification enable आहे का तपासा

---

## ✅ Deployment Checklist

Deploy करण्यापूर्वी हे सर्व तपासा:

- [ ] Code GitHub वर push केले आहे
- [ ] PostgreSQL database तयार केले आहे
- [ ] Web Service create केले आहे
- [ ] सर्व environment variables set केले आहेत
- [ ] `SECRET_KEY` generate केले आहे
- [ ] `DATABASE_URL` correctly set आहे
- [ ] Email credentials set केले आहेत
- [ ] Build successful आहे
- [ ] Database tables तयार केले आहेत
- [ ] Admin user create केले आहे

---

## 🎉 Success!

जर सर्व काही बरोबर केले असेल, तर आपले app live होईल:

**URL:** `https://secret-santa-2vyg.onrender.com` (किंवा आपले custom URL)

---

## 📞 मदत हवी असल्यास

- Render Documentation: [render.com/docs](https://render.com/docs)
- Render Status: [status.render.com](https://status.render.com)
- Support: Render Dashboard → Contact Support

---

**शुभेच्छा! 🎁 आपले Secret Santa app आता live आहे!**
