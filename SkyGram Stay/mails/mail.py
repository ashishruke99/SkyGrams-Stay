import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import random

def generate_otp():
    # Generate a random 4-digit OTP
    otp = ''.join(random.choices('0123456789', k=4))
    return otp

def generate_email(subject, recipient_name, otp):
    # Generate email content with OTP
    body = f"Hello {recipient_name}!\n\nYour OTP is: {otp}"
    return body

def send_email(to_address, subject, body):
    # Define email sender and SMTP server details
    from_address = 'ashish.22111218@viit.ac.in'
    smtp_server = 'smtp.gmail.com'
    smtp_port = 587
    smtp_username = 'ashish.22111218@viit.ac.in'
    smtp_password = 'rqpy cpbt nnof spvv'

    # Create message container
    msg = MIMEMultipart()
    msg['Subject'] = subject
    msg['From'] = from_address
    msg['To'] = to_address

    # Create the body of the message
    text_part = MIMEText(body, 'plain')

    # Attach plain text part to message container
    msg.attach(text_part)

    # Send the message via SMTP server
    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(smtp_username, smtp_password)
        server.sendmail(from_address, to_address, msg.as_string())

if __name__ == "__main__":
    to_address = input("Enter recipient's email address: ")
    subject = 'OTP Verification'
    recipient_name = 'Recipient'
    
    otp = generate_otp()
    body = generate_email(subject, recipient_name, otp)

    send_email(to_address, subject, body)
    print("Email sent successfully!")
