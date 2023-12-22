from flask import url_for
from flask_mail import Message
from coupons_manager import mail


def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message(
        subject="Password Reset Request",
        sender="noreply@demo.com",
        recipients=[user.email],
    )
    msg.body = f"""
        Password Reset request is generated
        The link is valid for 30 
        To reset password visit following link
             {url_for('users.reset_token',token=token,_external=True)}

        Valid only for 30 minutes
        If you did not make this request ignore it.

         """
    print(msg.body)
    mail.send(msg)
