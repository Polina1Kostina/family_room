from email.message import EmailMessage
from celery import Celery
from config import SMTP_PASSWORD, SMTP_USER
import smtplib

celery = Celery('tasks', broker='redis://localhost:6379')

SMTP_HOST = "smtp.gmail.com"
SMTP_PORT = 465


@celery.task
def send_email_invite_event(email, event):
    send_email = EmailMessage()
    send_email['subject'] = 'Приглашение на мероприятие'
    send_email['From'] = SMTP_USER
    send_email['To'] = email
    template = f'<html><body><p>Привет !!!<br> Вас пригласили на мероприятие {event} </p></body></html>'
    send_email.set_content(template, subtype='html')
    with smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT) as server:
        server.login(SMTP_USER, SMTP_PASSWORD)
        server.send_message(send_email)
