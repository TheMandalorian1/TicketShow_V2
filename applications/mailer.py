from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart 
from email.mime.text import MIMEText
import os
import smtplib

SMTP_SERVER_HOST= "localhost"
SMTP_SERVER_PORT= 1025
SENDER_ADDRESS = "support@ticketshow.com"
SENDER_PASSWORD = ""


def SendMemer(receiver, subject, message, content="text", attachment=None):

    msg = MIMEMultipart()
    msg['From'] = SENDER_ADDRESS
    msg['To'] = receiver
    msg['Subject'] = subject

    if content == "html":
        msg.attach(MIMEText(message, "html"))
    else:
        msg.attach(MIMEText(message, "plain"))

    if attachment:
        with open(attachment, 'rb') as attachment_:

            part = MIMEBase('application', 'octet-stream')
            part.set_payload(attachment_.read())

        part.add_header('Content-Disposition', f'attachment; filename="{os.path.basename(attachment)}"')

        encoders.encode_base64(part)
        msg.attach(part)

    server = smtplib.SMTP(host = SMTP_SERVER_HOST, port = SMTP_SERVER_PORT)

    server.login(SENDER_ADDRESS, SENDER_PASSWORD)
    server.send_message(msg)
    server.quit()

    return 'Mail Sent successfully !!'


def sendMail(reciever, subject, message):
    msg=MIMEMultipart()
    msg["From"] = SENDER_ADDRESS
    msg["To"] = reciever
    msg["Subject"] = subject

    msg.attach(MIMEText(message,"html"))
    
    s = smtplib.SMTP(host=SMTP_SERVER_HOST, port=SMTP_SERVER_PORT)
    s.login(SENDER_ADDRESS,SENDER_PASSWORD)

    s.send_message(msg)
    s.quit()
    return True



