from app import mail
from flask_mail import Message
from flask import render_template

def mail_payment_confirmation(email, first_name, message, new_address):
    msg = Message("Bekraftelse", sender='chilichallengeinfo@gmail.com', recipients=[email])
    msg.html = render_template("mail_payment_confirmation.html", first_name=first_name, message=message, new_address=new_address)
    mail.send(msg)

def mail_answer(email, ans_message, name):
    msg = Message("Svar fran " + name, sender='chilichallengeinfo@gmail.com', recipients=[email])
    msg.html = render_template('mailtest.html', ans_message=ans_message, name=name)
    mail.send(msg)

def mail_registration_confirmation(user):
    msg = Message("En het registrering ", sender='chilichallengeinfo@gmail.com', recipients=[user.email])
    msg.html = render_template('mail_registration_confirmation.html', user=user)
    mail.send(msg)

def mail_password(email, password):
    msg = Message("Nytt losenord", sender='chilichallengeinfo@gmail.com', recipients=[email])
    msg.html = render_template('password_mail.html', password=password)
    mail.send(msg)
