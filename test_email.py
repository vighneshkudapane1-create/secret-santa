from app import create_app
from app.utils.email_service import send_event_created_email
from app.models import Event, User


def main():
    app = create_app()

    with app.app_context():
        event = Event.query.first()
        user = User.query.first()

        if event and user:
            send_event_created_email(event, user)
            print("✅ Test email sent! Check your inbox (and spam).")
        else:
            print("❌ No Event/User found in database. Create at least one event and one user, then try again.")


if __name__ == "__main__":
    main()

