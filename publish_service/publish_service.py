import pika
import smtplib
from email.mime.text import MIMEText
from dotenv import load_dotenv
import os

load_dotenv()

SMTP_SERVER = os.getenv('SMTP_SERVER')
SMTP_PORT = int(os.getenv('SMTP_PORT'))
SMTP_USER = os.getenv('SMTP_USER')
SMTP_PASSWORD = os.getenv('SMTP_PASSWORD')
RECIPIENT_EMAIL = os.getenv('RECIPIENT_EMAIL')

def send_email(user, message):
    msg = MIMEText(f"От пользователя: {user}\nСообщение: {message}")
    msg['Subject'] = 'Новое сообщение'
    msg['From'] = SMTP_USER
    msg['To'] = RECIPIENT_EMAIL

    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.starttls()
        server.login(SMTP_USER, SMTP_PASSWORD)
        server.sendmail(SMTP_USER, RECIPIENT_EMAIL, msg.as_string())

def publish_message(ch, method, properties, body):
    user, message = body.decode().split(':', 1)
    send_email(user, message)
    ch.basic_ack(delivery_tag=method.delivery_tag)

def main():
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    channel.queue_declare(queue='publish_queue', durable=True)
    channel.basic_consume(queue='publish_queue', on_message_callback=publish_message)
    channel.start_consuming()

if __name__ == '__main__':
    main()