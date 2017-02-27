from app import app, db, models
from flask import render_template, request, session, url_for, flash, redirect, jsonify
from flask_login import login_user, logout_user, current_user, login_required
## from models import User, Book, Contactpost
from flask_login import LoginManager
import json
from .forms import UserForm, AddressForm
from .models import User, Product, UserHasUser


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
def select_friend():
    product_list = Product.query.all()
    return render_template('select_chili.html',
                           product_list=product_list)


@app.route('/select_friend', methods=["GET", "POST"])
def select_chili():
    address_form=AddressForm()
    #TODO: get global user and get the friends
    #friend_list=UserHasUser.
    if address_form.validate_on_submit():
        redirect('/index')

    return render_template('select_friend.html',
                           adress_form=address_form)

@app.route('/checkout', methods=["GET", "POST"])
def checkout():
    product_list = Product.query.all()
    address_form=AddressForm()
    address_form.product_id.choices=[(product.id, 'Välj') for product in product_list]

    if 'product_radio' in request.form:
        selected_product=request.form['product_radio']
        print(selected_product)




    return render_template('checkout_process.html',
                           product_list=product_list,
                           adress_form=address_form)
