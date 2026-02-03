# 🔒 Event Privacy Features

## Overview

Events now have privacy settings to control who can see and join them.

---

## Privacy Settings

### 1. Privacy Type

**Public Events:**
- ✅ Visible in event list
- ✅ Anyone with invite code can join (if allowed)
- ✅ Event details visible to all

**Private Events:**
- 🔒 Hidden from public event list
- 🔒 Only participants can see
- 🔒 Only admin can add participants (if public join disabled)

### 2. Visibility Settings

**All:**
- Event visible to everyone
- Details accessible to all users

**Participants Only:**
- Only participants can see event details
- Others see "Access Denied"

**Invite Only:**
- Only accessible with invite code
- Not visible in event list

### 3. Public Join Setting

**Allow Public Join:**
- ✅ Anyone with invite code can join
- Users can join via "Join Event" page

**Disable Public Join:**
- 🔒 Only admin can add participants
- Invite code alone not enough

---

## How to Use

### Creating Private Event

1. Go to "Create Event"
2. Fill event details
3. In **Privacy Settings** section:
   - Select **Privacy Type**: "Private"
   - Select **Visibility**: "Participants Only"
   - Uncheck **"Allow public joining"** (optional)
4. Create event

### Creating Public Event

1. Go to "Create Event"
2. Fill event details
3. In **Privacy Settings** section:
   - Select **Privacy Type**: "Public" (default)
   - Select **Visibility**: "All" (default)
   - Check **"Allow public joining"** (default)
4. Create event

---

## Access Control

### Who Can See Event?

- **Admin/Owner**: Always can see
- **Participants**: Always can see
- **Public Events**: Everyone can see
- **Private Events**: Only participants

### Who Can Join Event?

- **Public + Allow Join**: Anyone with invite code
- **Public + No Join**: Only admin can add
- **Private + Allow Join**: Anyone with invite code
- **Private + No Join**: Only admin can add

---

## Database Migration

If you have existing events, run:

```bash
python add_privacy_columns.py
```

This will:
- Add privacy columns to events table
- Set all existing events to "Public" (default)
- Preserve all existing data

---

## Privacy Badges

Events now show privacy badges:
- 🟢 **Public** - Green badge
- 🟡 **Private** - Yellow/Warning badge

---

## Examples

### Example 1: Office Secret Santa (Private)
- Privacy: Private
- Visibility: Participants Only
- Allow Join: Yes
- Result: Only office members with invite code can join

### Example 2: Public Community Event
- Privacy: Public
- Visibility: All
- Allow Join: Yes
- Result: Everyone can see and join with code

### Example 3: Exclusive Private Event
- Privacy: Private
- Visibility: Participants Only
- Allow Join: No
- Result: Only admin can add participants manually

---

## Security Features

✅ **Access Control**: Privacy checks on all routes
✅ **Visibility Control**: Who can see event details
✅ **Join Control**: Who can join events
✅ **Admin Override**: Admins can always access their events

---

## Files Modified

1. `app/models.py` - Added privacy columns
2. `app/routes/events.py` - Added privacy checks
3. `app/templates/events/create.html` - Added privacy form
4. `app/templates/events/view.html` - Show privacy badges
5. `app/templates/events/list.html` - Show privacy badges
6. `add_privacy_columns.py` - Migration script

---

## Testing

1. **Create Private Event:**
   - Set privacy to "Private"
   - Logout and try to view (should fail)
   - Login and join with code (should work if allowed)

2. **Create Public Event:**
   - Set privacy to "Public"
   - Should appear in event list
   - Anyone can join with code

3. **Test Visibility:**
   - Create event with "Participants Only"
   - Non-participants should see "Access Denied"

---

**Privacy features are now active! Run migration script if you have existing events! 🔒**
    