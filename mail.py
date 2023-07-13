import smtplib
import mail
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

mail_data = mail.read_from_json()

# Email configuration
sender_email = mail_data['sender_email']
receiver_email = mail_data['receiver_email']

# SMTP server configuration protocol
smtp_server = mail_data['smtp_server']
smtp_port = mail_data['sender_email']
smtp_username = mail_data['smtp_port']
smtp_password = mail_data['smtp_password']


def send_mail():

    subject = 'Process is down, please check'
    message = 'Hello, This is the email content.'

    # Create the email message
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject

    # Attach the message to the email
    msg.attach(MIMEText(message, 'plain'))

    # Create a secure connection to the SMTP server
    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(smtp_username, smtp_password)
        server.sendmail(sender_email, receiver_email, msg.as_string())
        print('Email sent successfully!')
