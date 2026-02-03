# 💬 Anonymous Messaging Feature Guide

## ✅ What Was Implemented

### Anonymous Messaging System

1. **Send Messages** - Send anonymous messages to Secret Santa recipient
2. **View Messages** - View all received messages
3. **Mark as Read** - Mark messages as read
4. **Delete Messages** - Delete received messages

---

## 🎯 Features

### 1. Send Anonymous Message
- **Route:** `/messages/event/<id>/send`
- **Access:** Only participants with assignments
- **Privacy:** Completely anonymous (receiver doesn't know sender)
- **Character Limit:** 1000 characters

### 2. View Messages
- **Route:** `/messages/event/<id>/messages`
- **Shows:** All received messages
- **Features:**
  - Unread count badge
  - Mark as read functionality
  - Delete messages
  - Timestamp display

### 3. Message Management
- Mark messages as read/unread
- Delete messages (only receiver can delete)
- Unread indicator
- Message timestamps

---

## 🔒 Security & Privacy

### Who Can Send Messages?
- ✅ Only participants with Secret Santa assignments
- ✅ Can only message their assigned receiver
- ✅ Must have active assignment

### Who Can View Messages?
- ✅ Only the receiver can see messages
- ✅ Messages are anonymous (sender hidden)
- ✅ Only visible within the event

### Privacy Features:
- ✅ Sender ID hidden from receiver
- ✅ Messages only visible to receiver
- ✅ Can delete own messages
- ✅ Event-level messaging only

---

## 📋 How to Use

### For Secret Santa Givers:

1. **Send Message:**
   - Go to event page
   - Click "Send Message" button
   - Type your anonymous message
   - Click "Send Anonymous Message"
   - ✅ Message sent!

2. **View Received Messages:**
   - Go to event page
   - Click "Messages" button
   - See all received messages
   - Mark as read or delete

### For Message Receivers:

1. **View Messages:**
   - Go to event page
   - Click "Messages" button
   - See all anonymous messages
   - Unread messages highlighted

2. **Manage Messages:**
   - Mark as read (removes "New" badge)
   - Delete unwanted messages
   - View timestamps

---

## 🎨 UI Features

### Message Display:
- ✅ Unread messages highlighted (blue border)
- ✅ "New" badge for unread messages
- ✅ Timestamp for each message
- ✅ Anonymous sender indicator
- ✅ Mark read / Delete buttons

### Send Message Form:
- ✅ Character counter (0/1000)
- ✅ Warning when approaching limit
- ✅ Privacy reminder
- ✅ Receiver name shown (for context)

---

## 📁 Files Created

1. `app/routes/messages.py` - Message routes
2. `app/templates/messages/view.html` - View messages page
3. `app/templates/messages/send.html` - Send message form

---

## 🔗 URLs

- `/messages/event/<id>/messages` - View messages
- `/messages/event/<id>/send` - Send message
- `/messages/message/<id>/read` - Mark as read (API)
- `/messages/message/<id>/delete` - Delete message

---

## ✅ Testing

1. **Create event and generate assignments**
2. **Login as participant with assignment**
3. **Go to event page**
4. **Click "Send Message"**
5. **Type and send message**
6. **Login as receiver**
7. **View messages**
8. **Mark as read / Delete**

---

## 🎯 Use Cases

### Use Case 1: Ask for Preferences
**Giver sends:**
"Hi! I got you for Secret Santa. Any hints about what you might like?"

**Receiver sees:**
Anonymous message with question

### Use Case 2: Confirm Gift
**Giver sends:**
"Just wanted to let you know I got your gift! Hope you like it!"

**Receiver sees:**
Anonymous confirmation message

---

## ⚠️ Important Notes

1. **Anonymous:** Sender identity is never revealed
2. **One-way:** Only giver can message receiver (not vice versa)
3. **Event-bound:** Messages only within event context
4. **Character Limit:** 1000 characters max
5. **Deletable:** Receiver can delete messages

---

**Anonymous Messaging is now live! Test it out! 💬**
