from app import app, db, models
from flask import render_template, request, session, url_for, flash, redirect, jsonify
from flask_login import login_user, logout_user, current_user, login_required
## from models import User, Book, Contactpost
from flask.ext.login import LoginManager
import json
from .forms import LoginForm
from .models import User


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
    form = LoginForm()

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
def signup():
    form =LoginForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, password=form.password.data)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('index'))

    return render_template('register.html', form=form)
