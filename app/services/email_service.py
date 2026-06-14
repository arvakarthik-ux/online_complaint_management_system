from flask_mail import Message
from flask import current_app
from ..extensions import mail


def send_email(subject, recipients, body):

    try:

        msg = Message(

            subject=subject,

            recipients=recipients,

            body=body,

            sender=current_app.config[
                "MAIL_DEFAULT_SENDER"
            ]
        )

        mail.send(msg)

        print("\nEMAIL SENT SUCCESSFULLY\n")

    except Exception as e:

        print(f"\nEMAIL ERROR: {e}\n")