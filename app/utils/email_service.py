"""
Email notification service
"""
from flask import render_template, current_app, has_request_context, url_for
from flask_mail import Message
from app import mail
from threading import Thread

def send_async_email(app, msg):
    """Send email asynchronously"""
    with app.app_context():
        try:
            mail.send(msg)
        except Exception as e:
            print(f"Error sending email: {str(e)}")

def send_email(subject, recipients, template, **kwargs):
    """Send email to recipients"""
    if not recipients:
        return False
    
    # Ensure recipients is a list
    if isinstance(recipients, str):
        recipients = [recipients]
    
    try:
        with current_app.app_context():
            # Add url_for helper to template context
            # Safe helper: when there's no active request (e.g. test scripts),
            # just return "#" instead of failing on URL building.
            def url_for_external(endpoint, **values):
                if not has_request_context():
                    return "#"
                values.setdefault('_external', True)
                return url_for(endpoint, **values)

            kwargs['url_for'] = url_for_external
            
            msg = Message(
                subject=subject,
                recipients=recipients,
                html=render_template(f'emails/{template}.html', **kwargs),
                sender=current_app.config.get('MAIL_USERNAME') or 'noreply@secretsanta.com'
            )
        
        # Send email asynchronously
        Thread(target=send_async_email, args=(current_app._get_current_object(), msg)).start()
        return True
    except Exception as e:
        print(f"Error preparing email: {str(e)}")
        return False

def send_event_created_email(event, creator):
    """Send email when event is created"""
    subject = f"🎁 Secret Santa Event Created: {event.event_name}"
    recipients = [creator.email]
    
    send_email(
        subject=subject,
        recipients=recipients,
        template='event_created',
        event=event,
        creator=creator
    )

def send_assignment_email(assignment, giver, receiver, event):
    """Send email when assignment is generated"""
    subject = f"🎁 Your Secret Santa Assignment for {event.event_name}"
    recipients = [giver.email]
    
    send_email(
        subject=subject,
        recipients=recipients,
        template='assignment_notification',
        assignment=assignment,
        giver=giver,
        receiver=receiver,
        event=event
    )

def send_new_message_email(message, receiver, sender_name, event):
    """Send email when new message is received"""
    subject = f"💬 New Anonymous Message - {event.event_name}"
    recipients = [receiver.email]
    
    send_email(
        subject=subject,
        recipients=recipients,
        template='new_message',
        message=message,
        receiver=receiver,
        sender_name=sender_name,
        event=event
    )

def send_deadline_reminder_email(event, participant):
    """Send email reminder for gift deadline"""
    subject = f"⏰ Gift Deadline Reminder - {event.event_name}"
    recipients = [participant.user.email]
    
    send_email(
        subject=subject,
        recipients=recipients,
        template='deadline_reminder',
        event=event,
        participant=participant
    )

def send_event_status_email(event, participant, status):
    """Send email when event status changes"""
    subject = f"📢 Event Update: {event.event_name} - {status.title()}"
    recipients = [participant.user.email]
    
    send_email(
        subject=subject,
        recipients=recipients,
        template='event_status',
        event=event,
        participant=participant,
        status=status
    )

def send_participant_joined_email(event, new_participant, admin):
    """Send email to admin when new participant joins"""
    subject = f"👤 New Participant Joined: {event.event_name}"
    recipients = [admin.email]
    
    send_email(
        subject=subject,
        recipients=recipients,
        template='participant_joined',
        event=event,
        new_participant=new_participant,
        admin=admin
    )
