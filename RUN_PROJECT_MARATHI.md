# 🚀 Secret Santa - प्रोजेक्ट चालवण्यासाठी Commands (मराठी)

## ⚡ जलद सुरुवात - Commands

### Step 1: Command Prompt उघडा
`Win + R` दाबा, `cmd` टाइप करा, Enter दाबा

### Step 2: प्रोजेक्ट फोल्डरमध्ये जा
```bash
cd C:\wamp64\www\secrete-santa
```

### Step 3: Virtual Environment Activate करा
```bash
venv\Scripts\activate
```

**अपेक्षित Output:**
```
(venv) C:\wamp64\www\secrete-santa>
```

### Step 4: Application चालवा
```bash
python run.py
```

**अपेक्षित Output:**
```
 * Running on http://0.0.0.0:5000
 * Debug mode: on
```

### Step 5: Browser मध्ये उघडा
Browser उघडा आणि जा:
```
http://localhost:5000
```

---

## 📋 पूर्ण Setup Commands (पहिल्यांदा फक्त)

### जर Virtual Environment तयार नसेल:
```bash
cd C:\wamp64\www\secrete-santa
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

### जर Database Tables तयार नसतील:
```bash
python create_tables.py
```

### जर Sample Data Insert नसेल:
```bash
python sample_data_insert.py
```

---

## 🎯 सर्व Commands एकत्र (Copy-Paste करा)

हे commands एक-एक करून copy-paste करा:

```bash
# प्रोजेक्ट फोल्डरमध्ये जा
cd C:\wamp64\www\secrete-santa

# Virtual Environment Activate करा
venv\Scripts\activate

# Application चालवा
python run.py
```

---

## ⏹️ Server थांबवणे

Command Prompt मध्ये `Ctrl + C` दाबा.

---

## 🔧 समस्या निराकरण Commands

### जर "ModuleNotFoundError" येत असेल:
```bash
venv\Scripts\activate
pip install -r requirements.txt
```

### जर "Port 5000 already in use" येत असेल:
`run.py` file edit करा आणि port 5001 करा, नंतर:
```bash
python run.py
```

### जर "Can't connect to MySQL" येत असेल:
1. WAMP चालू आहे का तपासा (GREEN icon)
2. phpMyAdmin मध्ये database आहे का तपासा
3. `config.py` मध्ये settings तपासा

---

## 📝 Quick Reference Table

| काम | Command |
|------|---------|
| प्रोजेक्ट फोल्डरमध्ये जा | `cd C:\wamp64\www\secrete-santa` |
| Virtual Environment Activate | `venv\Scripts\activate` |
| Application चालवा | `python run.py` |
| Tables तयार करा | `python create_tables.py` |
| Sample Data Insert करा | `python sample_data_insert.py` |
| Packages Install करा | `pip install -r requirements.txt` |
| Server थांबवा | `Ctrl + C` |

---

## 🌐 Access URLs

- **Application:** http://localhost:5000
- **phpMyAdmin:** http://localhost/phpmyadmin

---

## ✅ Success Checklist

Application चालू आहे का तपासण्यासाठी:

- ✅ Command Prompt मध्ये `Running on http://0.0.0.0:5000` दिसत आहे
- ✅ Browser मध्ये `http://localhost:5000` उघडत आहे
- ✅ Login/Register page दिसत आहे
- ✅ कोणतीही error message नाही

---

## 💡 Tips

1. **पहिल्यांदा:** सर्व setup commands run करा
2. **दर वेळी:** फक्त `venv\Scripts\activate` आणि `python run.py` run करा
3. **Error आल्यास:** Command Prompt मधील error message वाचा
4. **Port बदल:** जर 5000 port busy असेल, `run.py` मध्ये port बदला

---

**तयार! आता तुमची Application चालू आहे! 🎁🎄**
