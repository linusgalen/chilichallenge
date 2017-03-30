from app import mail
from flask_mail import Message
from flask import render_template

def mail_payment_confirmation(email, first_name, message, new_address):
    msg = Message("Bekraftelse", sender='chilichallengeinfo@gmail.com', recipients=[email])
    msg.html = render_template("mail_payment_confirmation.html", first_name=first_name, message=message, new_address=new_address)
    mail.send(msg)

def mail_answer(email, ans_message, name):
    msg = Message("Svar från " + name, sender='chilichallengeinfo@gmail.com', recipients=[email])
    msg.html = render_template('mailtest.html', ans_message=ans_message, name=name)
    mail.send(msg)

def mail_password(email, password):
    msg = Message("Nytt lösenord", sender='chilichallengeinfo@gmail.com', recipients=[email])
    msg.html = render_template('password_mail.html', password=password)
    mail.send(msg)

