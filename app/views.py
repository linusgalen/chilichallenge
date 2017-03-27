# coding=utf-8
import random
import string

from app import app, db, models, stripe_keys
from flask import render_template, request, session, url_for, flash, redirect, jsonify, g
from flask_login import login_user, logout_user, current_user, login_required
from flask_login import LoginManager
import json
import stripe
from stripe import api_key
from datetime import datetime
from .models import User, Product, UserHasUser, Address, Challenge
from .forms import RegisterForm, AddressForm


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
    if request.method == 'GET':
        return render_template('login_validation.html')
    user = User.query.filter_by(username = request.form['username'], password = request.form['password']).first()
    if user is None:
        flash("Användarnamn eller lösenord är fel!")
        return redirect(url_for('login'))
    login_user(user)
    flash('Logged in successfully', 'success')
    return redirect(url_for('index'))

@app.route('/signout')
def signout():
    logout_user()

    return redirect(url_for('index'))

@app.route('/register', methods=["GET", "POST"])
def register():
    user_valid = True
    email_valid = True
    if request.method == 'GET':
        return render_template('register.html',
                               user_valid = user_valid,
                               email_valid = email_valid)
    username = request.form['username']
    user_check = User.query.filter_by(username = username).first()
    if user_check is not None:
        user_valid = False
    email = request.form['email']

    print('email:'+email+' usrname:'+username)


    email_check = User.query.filter_by(email = email).first()
    if email_check is not None:
        email_valid = False
    if user_check is not None or email_check is not None:
        print('hello')
        return render_template('register.html',
                               user_valid = user_valid,
                               email_valid = email_valid)
    user = User(username=username, password=request.form['password'], email=email)
    db.session.add(user)
    db.session.commit()

    return redirect(url_for('index'))


@app.route('/charge', methods=['POST'])
def charge():

    token_id = request.form['tokenId']
    email=request.form['email']
    product_id=request.form['productId']

    #Address
    first_name=request.form['firstName']
    last_name=request.form['lastName']
    address=request.form['address']
    city=request.form['city']
    zip=request.form['zip']
    message=request.form['message']


    bought_product=db.session.query(Product).get(product_id)

    new_address=Address(
        zip=zip,
        last_name=last_name,
        first_name=first_name,
        city=city,
        address=address,
        email=email
    )
    db.session.add(new_address)
    db.session.commit()

    #Make sure challenge_code is unique
    flag=True
    while flag:
        length=5
        challenge_code=''.join(random.SystemRandom().choice(string.ascii_lowercase + string.digits) for _ in range(length))
        test_challenge = Challenge.query.filter_by(challenge_code=challenge_code).first()
        if test_challenge is None:
            flag=False


    print(challenge_code)

    new_challenge=Challenge(
        message=message,
        address_id=new_address.id,
        product_id=product_id,
        datetime=datetime.now(),
        challenge_code=challenge_code
    )
    db.session.add(new_challenge)
    db.session.commit()


    amount=int(bought_product.price)*100

    customer = stripe.Customer.create(
        email=email,
        source=token_id
    )

    charge = stripe.Charge.create(
        customer=customer.id,
        amount=amount,
        currency='SEK',
        description=bought_product.name
    )

    #TODO Send confirmation Email

    return render_template('charge.html',
                           email=email,
                           product=bought_product,
                           address=new_address)




if __name__ == '__main__':
    app.run(debug=True)


@app.route('/select_friend', methods=["GET", "POST"])
def select_chili():
    address_form = AddressForm()
    # TODO: get global user and get the friends
    # friend_list=UserHasUser.
    if address_form.validate_on_submit():
        redirect('/index')

    return render_template('select_friend.html',
                           adress_form=address_form)

@app.route('/checkout', methods=["GET", "POST"])
def checkout():
    product_list = Product.query.all()
    # address_form=AddressForm()

    if 'first_name' in request.form:
        first_name = request.form['first_name']

    if 'last_name' in request.form:
        last_name = request.form['last_name']

    if 'street_address' in request.form:
        street_address = request.form['street_address']

    if 'zipcode' in request.form:
        zipcode = request.form['zipcode']

    # address_form.product_id.choices=[(product.id, 'Valj') for product in product_list]
    key = 'pk_test_Y2poyAHtZzOY2qOmdqvzvizu'

    if 'product_radio' in request.form:
        selected_product = request.form['product_radio']
        print(selected_product)

    if 'message' in request.form:
        message = request.form['message']

    return render_template('checkout_process.html',
                           product_list=product_list,
                           key=key)

@app.route('/profile', methods=["GET", "POST"])
def profile_page():

    # current_address = Address.query.filter_by(id = g.user.address_id).first();
    challenge_list = Challenge.query.filter_by(user_id = g.user.id).all();


    return render_template('profile_page.html',
                           current_user = g.user,
                           # current_address = current_address,
                           challenge_list = challenge_list,
                           key=api_key)


@app.route('/confirm')
def confirm():
    return render_template('checkout_layout.html')


@app.route('/aboutchili', methods=["GET"])
def aboutchili():
    product_list = Product.query.all()
    return render_template('aboutchili.html',
                           product_list=product_list)


@app.route('/aboutchili/<int:product_id>')
def product(product_id):
    product = db.session.query(Product).get(product_id).seralize
    return jsonify(product)
