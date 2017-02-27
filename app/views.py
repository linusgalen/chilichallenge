from app import app, db, models
from flask import render_template, request, session, url_for, flash, redirect, jsonify, g
from flask_login import login_user, logout_user, current_user, login_required
## from models import User, Book, Contactpost
from flask_login import LoginManager
import json
from .forms import RegisterForm
from .models import User, Product, Address

@app.before_request
def before_request():
    g.user = current_user


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
    form = RegisterForm()

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
    form =RegisterForm()
    if form.validate_on_submit():
        address = Address(first_name=form.first_name.data, last_name=form.last_name.data, address=form.address.data, zip=form.zip.data, city=form.city.data , email=form.email.data)
        db.session.add(address)
        db.session.commit()
        user = User(username=form.username.data, password=form.password.data, email=form.email.data, address_id=address.id )
        db.session.add(user)
        db.session.commit()

        return redirect(url_for('index'))

    return render_template('register.html', form=form)


@app.route('/select', methods=["GET"])
def select_chili():
    product_list = Product.query.all()
    return render_template('select_chili.html',
                           product_list=product_list)
