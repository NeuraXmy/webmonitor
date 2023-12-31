import threading
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from flask import current_app, render_template
from webmonitor.utils.error import ErrorCode, abort

def send_email(to, subject, template, **kwargs):
    current_app.logger.info(f"send email to {to} with subject={subject} template={template}")
    html = render_template(template, **kwargs)
    config = current_app.config
    email_thread = threading.Thread(target=send_email_thread, args=(to, subject, html, config))
    email_thread.start()

def send_email_thread(to, subject, html, config):
    smtp_server   = config['MAIL_SERVER']
    smtp_port     = config['MAIL_PORT']
    smtp_username = config['MAIL_USERNAME']
    smtp_password = config['MAIL_PASSWORD']
    from_addr     = config['MAIL_SENDER']

    msg = MIMEMultipart()
    msg['From'] = from_addr
    msg['To'] = to
    msg['Subject'] = subject

    body = MIMEText(html, 'html')
    msg.attach(body)

    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(smtp_username, smtp_password)
            server.send_message(msg)
            server.quit()
    except Exception as e:
        abort(ErrorCode.EMAIL_SEND_FAIL, msg=f"邮件发送失败: {e}")