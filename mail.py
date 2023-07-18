import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import json

# Open the JSON file
with open('mail_config.json', 'r') as file:
    # Load the JSON data
    mail_data = json.load(file)

with open('mail_templates.json', 'r') as file:
    # Load the JSON data
    mail_lang = json.load(file)

# Email configuration
sender_email = mail_data['sender_email']
receiver_email = mail_data['receiver_email']

# SMTP server configuration protocol
smtp_server = mail_data['smtp_server']
smtp_port = mail_data['smtp_port']
smtp_username = mail_data['smtp_username']
smtp_password = mail_data['smtp_password']


def send_mail(name='', call_type=''):

    if not mail_data:
        return ()

    if name:
        if call_type == "process":
            subject = mail_lang['process_subject']
            message = mail_lang['process_message'] + str(name)

        if call_type == "service":
            subject = mail_lang['service_subject']
            message = mail_lang['service_message'] + str(name)
    else:
        print("Error, function called with no name")
        return 0

    # Create the email message
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject
    # print(mail_data)

    # Attach the message to the email
    msg.attach(MIMEText(message, 'plain'))
    server = smtplib.SMTP_SSL(f"{smtp_server}:{smtp_port}")
    server.login(smtp_username, smtp_password)
    server.sendmail(sender_email, receiver_email, msg.as_string())
    server.quit()

