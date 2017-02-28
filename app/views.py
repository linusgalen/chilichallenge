from app import app, db, models
from flask import render_template, request, session, url_for, flash, redirect, jsonify, g
from flask_login import login_user, logout_user, current_user, login_required
## from models import User, Book, Contactpost
from flask_login import LoginManager
import json
from .forms import RegisterForm, LoginForm
from .models import User, Product, Address, Challenge

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
    if g.user is not None and g.user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username, password=password).first()

        if user is not None:
            login_user(user)
            flash('Logged in successfully.')
            session['remember_me'] = form.remember_me.data
            return redirect(url_for('index'))
        else:
            flash("Username or password incorrect!")
            return render_template('login.html',
                                   title='Sign In',
                                   form=form)

    return render_template('login.html',
                       title='Logga in',
                       form=form)
# if user.is_correct_password(password):


# else:
#flash('Fel användarnamn eller lösenord')
#return redirect(url_for('login'))



@app.route('/signout')
def signout():
    logout_user()

    return redirect(url_for('login'))

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

@app.route('/profile', methods=["GET", "POST"])
def profile_page():

    # if load_user!=None:
    #     return redirect (url_for('login'))
    # else:
    current_address = Address.query.filter_by(id = g.user.address_id).first();
    #Here are we <3 gullungar
    user_orders = Challenge.query.filter(user_id = g.user.id);
    return render_template('profile_page.html',
                           current_user = g.user,
                           current_address = current_address)
