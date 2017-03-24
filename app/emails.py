from app import mail
from flask_mail import Message
from flask import render_template

def mail_payment_confirmation(email, first_name, message):
    msg = Message("Bekraftelse", sender='chilichallengeinfo@gmail.com', recipients=[email])
    msg.html = render_template("mail_payment_confirmation.html", first_name=first_name, message=message)
    mail.send(msg)

