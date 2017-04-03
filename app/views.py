# coding=utf-8
import random
import string

from app import app, db, models, stripe_keys, mail, emails
from flask import render_template, request, session, url_for, flash, redirect, jsonify, g
from flask_login import login_user, logout_user, current_user, login_required
from flask_login import LoginManager
import json
import stripe
from stripe import api_key
from .models import User, Product, UserHasUser, Address, Challenge, Order
from datetime import datetime
from .models import User, Product, UserHasUser, Address, Challenge


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
    username_valid=True
    password_valid=True

    if g.user is not None and g.user.is_authenticated:
        return redirect(url_for('index'))
    if request.method == 'GET':
        return render_template('login.html',
                               username_valid=username_valid,
                               password_valid=password_valid)

    user = User.query.filter_by(username = request.form['username'], password = request.form['password']).first()
    if user is None:
        user = User.query.filter_by(username=request.form['username']).first()
        if user is None:
            username_valid=False
        else:
            password_valid=False

        return render_template('login.html',
                               username_valid=username_valid,
                               password_valid=password_valid)

    login_user(user)
    return redirect(url_for('index'))

@app.route('/recover_password', methods=["GET", "POST"])
def recover_password():
    valid = False
    not_valid = False
    if g.user is not None and g.user.is_authenticated:
        return redirect(url_for('index'))
    if request.method == 'GET':
        return render_template('recover_password.html',
                               valid = valid,
                               not_valid = not_valid)

    if not 'send_mail' in request.form:
        user = User.query.filter_by(username=request.form['recPassword']).first()

        if user is not None:
            valid = True
            session['user_changer'] = user.id
        else:
            user = User.query.filter_by(email=request.form['recPassword']).first()
        if user is not None:
            valid = True
            session['user_changer'] = user.id
        else:
            not_valid = True
        return render_template('recover_password.html',
                               valid=valid,
                               not_valid=not_valid,
                               user=user)
    else:
        length = 8
        new_password = ''.join(random.SystemRandom().choice(string.ascii_lowercase + string.digits) for _ in range(length))
        user_temp = session['user_changer']
        user = User.query.filter_by(id = user_temp).first()
        user.password = new_password

        db.session.commit()

        emails.mail_password(user.email, user.password)
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

    email_check = User.query.filter_by(email = email).first()
    if email_check is not None:
        email_valid = False
    if user_check is not None or email_check is not None:
        return render_template('register.html',
                               user_valid = user_valid,
                               email_valid = email_valid)

    user = User(username=username, password=request.form['password'], email=email)
    db.session.add(user)
    db.session.commit()
    login_user(user)

    emails.mail_registration_confirmation(user)

    return redirect(url_for('index'))

@app.route('/change_userinfo', methods=["GET", "POST"])
def change_userinfo():
    user_valid = True
    email_valid = True
    if request.method == 'GET':
        return render_template('change_userinfo.html',
                               user_valid = user_valid,
                               email_valid = email_valid,
                               password = True,
                               pas_valid = True)
    if 'pasbtn' in request.form:
        if request.form['checkpassword'] != g.user.password:
            return render_template('change_userinfo.html',
                                   user_valid = user_valid,
                                   email_valid = email_valid,
                                   password = True,
                                   pas_valid = False)
        else:
            return render_template('change_userinfo.html',
                                   user_valid = user_valid,
                                   email_valid = email_valid,
                                   password = False,
                                   curusername = g.user.username,
                                   curemail = g.user.email)
    username = request.form['username']
    user_check = User.query.filter_by(username = username).first()
    if user_check is not None and user_check.username != g.user.username:
        user_valid = False
    email = request.form['email']

    email_check = User.query.filter_by(email = email).first()
    if email_check is not None and email_check.email != g.user.email:
        email_valid = False
    if user_valid == False or email_valid == False:
        return render_template('change_userinfo.html',
                               user_valid = user_valid,
                               email_valid = email_valid,
                               password = False,
                               curusername = g.user.username,
                               curemail = g.user.email)

    g.user.username = username
    g.user.email = email
    g.user.password = request.form['password']
    db.session.commit()

    return redirect(url_for('profile_page'))


@app.route('/aboutcc', methods=['GET'])
def yolo():
    return render_template('aboutCC.html')

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

    if g.user is not None and g.user.is_authenticated:
        emails.mail_payment_confirmation(email, g.user.username, message, new_address)
    else:
        emails.mail_payment_confirmation(email, first_name, message, new_address)

    return render_template('charge.html',
                           email=email,
                           product=bought_product,
                           address=new_address)




if __name__ == '__main__':
    app.run(debug=True)



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



@app.route('/challenged', methods =["GET", "POST"])
def challenged():
    if request.method == 'POST':

        if 'message_button' in request.form:
            challenge_id = Challenge.query.filter_by(challenge_code=request.form['generated_code']).first()

            if challenge_id is None:
                return render_template('been_challenged.html', show_enter_code = True )

            session['challenge_id'] = challenge_id.id
            return render_template('been_challenged.html', message=challenge_id.message, show_message_answer=True, email = challenge_id.address.email,  answer_message = challenge_id.answer_message)

        if 'answer_button' in request.form:
            chal = Challenge.query.filter_by(id=session['challenge_id']).first()
            chal.answer_message = request.form['answer_message']
            db.session.commit()
            emails.mail_answer(chal.address.email, chal.answer_message, chal.address.first_name + ' ' + chal.address.last_name)
            return render_template('been_challenged.html', show_email_have_been_sent_page=True, email=chal.address.email)

    return render_template('been_challenged.html', show_enter_code=True)


