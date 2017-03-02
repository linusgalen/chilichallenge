from app import app, db, models
from flask import render_template, request, session, url_for, flash, redirect, jsonify, g
from flask_login import login_user, logout_user, current_user, login_required
from flask_login import LoginManager
import json
from stripe import api_key

from .models import User, Product, UserHasUser, Address, Challenge
from .forms import RegisterForm, LoginForm, AddressForm



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
#flash('Fel anvandarnamn eller losenord')
#return redirect(url_for('login'))



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
    address_form.product_id.choices=[(product.id, 'Valj') for product in product_list]

    if 'product_radio' in request.form:
        selected_product=request.form['product_radio']
        print(selected_product)



    return render_template('checkout_process.html',
                           product_list=product_list,
                           adress_form=address_form)

@app.route('/profile', methods=["GET", "POST"])
def profile_page():

    # if load_user!=None:
    #     return redirect (url_for('login'))
    # else:
    current_address = Address.query.filter_by(id = g.user.address_id).first();
    challenge_list = Challenge.query.filter_by(user_id = g.user.id).all();


    return render_template('profile_page.html',
                           current_user = g.user,
                           current_address = current_address,
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
    product =db.session.query(Product).get(product_id).seralize
    return jsonify(product)

