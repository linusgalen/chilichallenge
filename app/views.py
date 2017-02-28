from app import app, db, models
from flask import render_template, request, session, url_for, flash, redirect, jsonify
from flask_login import login_user, logout_user, current_user, login_required
## from models import User, Book, Contactpost
from flask_login import LoginManager
import json
from .forms import UserForm
from .models import User, Product


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


@app.route('/select', methods=["GET"])
def select_chili():
    product_list = Product.query.all()
    return render_template('select_chili.html',
                           product_list=product_list)

@app.route('/profile', methods=["GET", "POST"])
def profile_page():

    # if load_user!=None:
    #     return redirect (url_for('login'))
    # else:

    current_user=User.query.get(int(id))

    return render_template('profile_page.html',
                           current_user=current_user)
