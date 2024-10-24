import smtplib
import imghdr
from email.message import EmailMessage
import os

SENDER_EMAIL = os.getenv("EMAILUSERNAME")
PASSWORD = os.getenv("PASSWORD2")
RECEIVER = os.getenv("EMAILUSERNAME")


def send(image_path):
    email_message = EmailMessage
    email_message["Subject"] = "New Camera Alert!"
    email_message.set_content("New activity on your camera!")

    with open(image_path, "rb") as file:
        content = file.read()

    email_message.add_attachment(content, maintype="image", subtype=imghdr.what(None, content))

    gmail = smtplib.SMTP("smtp.gmail.com", 587)
    gmail.ehlo()
    gmail.starttls()
    gmail.login(SENDER_EMAIL, PASSWORD)
    gmail.sendmail(SENDER_EMAIL, RECEIVER, email_message.as_string())
    gmail.quit()

