# 🔒 Privacy Features Setup Guide

## ✅ What Was Added

### Privacy Settings for Events:
1. **Privacy Type**: Public or Private
2. **Visibility**: All, Participants Only, or Invite Only
3. **Public Join**: Allow/disallow joining with invite code

---

## 🚀 Setup Steps

### Step 1: Add Privacy Columns to Database

If you have existing database, run:

```bash
python add_privacy_columns.py
```

**OR** if starting fresh, the updated `database_schema.sql` already includes privacy columns.

### Step 2: Restart Application

```bash
python run.py
```

### Step 3: Test Privacy Features

1. **Create Private Event:**
   - Go to Create Event
   - Set Privacy: "Private"
   - Set Visibility: "Participants Only"
   - Create event

2. **Test Access:**
   - Logout
   - Try to view event (should fail)
   - Login and join with code (should work)

---

## 📋 Privacy Options Explained

### Privacy Type

**Public:**
- Event appears in event list
- Anyone can see event details
- Default setting

**Private:**
- Event hidden from public list
- Only participants can see
- More secure

### Visibility

**All:**
- Everyone can see event
- Default setting

**Participants Only:**
- Only participants can see details
- Others get "Access Denied"

**Invite Only:**
- Only accessible with invite code
- Not in public list

### Allow Public Join

**Checked (Yes):**
- Anyone with invite code can join
- Users can self-join

**Unchecked (No):**
- Only admin can add participants
- More control

---

## 🎯 Use Cases

### Use Case 1: Office Secret Santa (Private)
```
Privacy: Private
Visibility: Participants Only
Allow Join: Yes
```
- Only office members can see
- They can join with invite code
- Secure and private

### Use Case 2: Public Community Event
```
Privacy: Public
Visibility: All
Allow Join: Yes
```
- Everyone can see
- Anyone can join with code
- Open and accessible

### Use Case 3: Exclusive Event (Very Private)
```
Privacy: Private
Visibility: Participants Only
Allow Join: No
```
- Only admin can add participants
- Completely private
- Maximum control

---

## ✅ Verification

After setup, verify:

1. ✅ Can create events with privacy settings
2. ✅ Privacy badges show on events
3. ✅ Private events hidden from non-participants
4. ✅ Access control works correctly
5. ✅ Join restrictions work

---

## 🔧 Files Modified

1. `app/models.py` - Added privacy columns
2. `app/routes/events.py` - Added privacy checks
3. `app/templates/events/create.html` - Privacy form
4. `app/templates/events/view.html` - Privacy badges
5. `app/templates/events/list.html` - Privacy badges
6. `database_schema.sql` - Updated schema
7. `add_privacy_columns.py` - Migration script

---

**Run `python add_privacy_columns.py` to add privacy to existing database! 🔒**
