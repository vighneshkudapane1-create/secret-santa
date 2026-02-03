# 🚀 Secret Santa - Project Run Commands

## Quick Start Commands

### Step 1: Open Command Prompt
Press `Win + R`, type `cmd`, press Enter

### Step 2: Navigate to Project Folder
```bash
cd C:\wamp64\www\secrete-santa
```

### Step 3: Activate Virtual Environment
```bash
venv\Scripts\activate
```

**Expected Output:**
```
(venv) C:\wamp64\www\secrete-santa>
```

### Step 4: Run the Application
```bash
python run.py
```

**Expected Output:**
```
 * Running on http://0.0.0.0:5000
 * Debug mode: on
```

### Step 5: Open in Browser
Open browser and go to:
```
http://localhost:5000
```

---

## Complete Setup Commands (First Time Only)

### If Virtual Environment Not Created:
```bash
cd C:\wamp64\www\secrete-santa
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

### If Database Tables Not Created:
```bash
python create_tables.py
```

### If Sample Data Not Inserted:
```bash
python sample_data_insert.py
```

---

## All-in-One Command Sequence

Copy and paste these commands one by one:

```bash
# Navigate to project
cd C:\wamp64\www\secrete-santa

# Activate virtual environment
venv\Scripts\activate

# Run application
python run.py
```

---

## Stop the Server

Press `Ctrl + C` in the command prompt to stop the server.

---

## Troubleshooting Commands

### If "ModuleNotFoundError":
```bash
venv\Scripts\activate
pip install -r requirements.txt
```

### If "Port 5000 already in use":
Edit `run.py` and change port to 5001, then:
```bash
python run.py
```

### If "Can't connect to MySQL":
1. Check WAMP is running (GREEN icon)
2. Verify database exists in phpMyAdmin
3. Check `config.py` settings

---

## Quick Reference

| Task | Command |
|------|---------|
| Navigate to project | `cd C:\wamp64\www\secrete-santa` |
| Activate venv | `venv\Scripts\activate` |
| Run app | `python run.py` |
| Create tables | `python create_tables.py` |
| Insert data | `python sample_data_insert.py` |
| Install packages | `pip install -r requirements.txt` |
| Stop server | `Ctrl + C` |

---

## Access URLs

- **Application:** http://localhost:5000
- **phpMyAdmin:** http://localhost/phpmyadmin

---

**That's it! Your application should now be running! 🎁**
