from app import app, db, models
from flask import render_template, request, session, url_for, flash, redirect, jsonify, g
from flask_login import login_user, logout_user, current_user, login_required
## from models import User, Book, Contactpost
from flask_login import LoginManager
import json
from .forms import UserForm
from .models import User, Product
import logging

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')


login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))


@app.route('/login', methods=["GET", "POST"])
def login():
    form = UserForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first_or_404()
        if user.is_correct_password(form.password.data):
            login_user(user)

            return redirect(url_for('index'))
        else:
            return redirect(url_for('login'))
    return render_template('login.html', form=form)

@app.route('/signout')
def signout():
    logout_user()

    return redirect(url_for('index'))

@app.route('/register', methods=["GET", "POST"])
def register():
    form =UserForm()
    if form.validate_on_submit():
        user = User(name=form.name.data,username=form.username.data,address=form.address.data,
                    zipcode=form.zipcode.data,city=form.city.data,password=form.password.data)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('index'))

    return render_template('register.html', form=form)


@app.route('/checkout')
#an input parameter to this function MUST be some kind of order ID
def checkout():
    logging.warning("hej") #just testing som stuff.

    amount = 1000
    #should 1: retreive product data from the database.
    #should 2: send this data as a parameter to the template renderer.
    #should 3: compute price here, and send it in to template rendered for display.

    return render_template('checkout.html', amount = amount)

@app.route('/charge', methods=['POST'])
def charge():
    # Amount in cents
    amount = 10000
    username = g.user.username

    customer = stripe.Customer.create(
        email='customer@example.com',
        source=request.form['stripeToken']
    )

    charge = stripe.Charge.create(
        customer=customer.id,
        amount=amount,
        currency='usd',
        description='Flask Charge'
    )

    return render_template('charge.html', amount=amount)

if __name__ == '__main__':
    app.run(debug=True)

@app.route('/select', methods=["GET"])
def select_chili():
    product_list = Product.query.all()
    return render_template('select_chili.html',
                           product_list=product_list)

@app.route('/profile', methods=["GET", "POST"])
def profile_page():
    if load_user!=None:
        return redirect(url_for('login'))
    else:
        current_user=User.query.get(int(id))

    return render_template('profile_page.html',
                           current_user=current_user)
