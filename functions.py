import os
import smtplib
from email.message import EmailMessage
from datetime import datetime
import imghdr
import glob

PASSWORD = os.environ.get("PASSWORD_GMAIL")
SENDER = "alexlerch76@gmail.com"
RECEIVER = "alexlerch76@gmail.com"


def send_mail(image_path):
    email_message = EmailMessage()
    email_message["Subject"] = "New costumer showed up!"
    email_message.set_content("Hey, we just saw a new customer!")

    with open(image_path, "rb") as file:
        content = file.read()

    email_message.add_attachment(content, maintype="image", subtype=imghdr.what(None, content))

    gmail = smtplib.SMTP("smtp.gmail.com", 587)
    gmail.ehlo()
    gmail.starttls()
    gmail.login(SENDER, PASSWORD)
    gmail.sendmail(SENDER, RECEIVER, email_message.as_string())
    gmail.quit()


def clean_folder():
    images = glob.glob("images/*.png")
    for image in images:
        os.remove(image)


if __name__ == "__main__":
    send_mail(image_path="images/19.png")