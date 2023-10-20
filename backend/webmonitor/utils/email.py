from flask_mail import Mail, Message
from flask import current_app, render_template


def send_email(to, subject, template, **kwargs):
    mail = Mail(current_app)
    msg = Message(subject=subject, recipients=[to], sender=current_app.config['MAIL_USERNAME'])
    msg.html = render_template(template, **kwargs)
    mail.send(msg)

