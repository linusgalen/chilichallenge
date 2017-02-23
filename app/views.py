from app import app, db, models
from flask import render_template, request, session, url_for, flash, redirect, jsonify
from flask_login import login_user, logout_user, current_user, login_required
## from models import User, Book, Contactpost
from flask_login import LoginManager
import json


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
