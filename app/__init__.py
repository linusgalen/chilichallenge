from flask import Flask, Response, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_basicauth import BasicAuth
from flask_admin import Admin
from flask_admin.contrib import sqla
from flask_login import LoginManager
import os
import stripe

stripe_keys = {
  'secret_key': 'sk_test_xiZrTPRhV7otP7ZjRE0FOK2Z', #os.environ['SECRET_KEY'],
  'publishable_key': 'pk_test_Y2poyAHtZzOY2qOmdqvzvizu' #os.environ['PUBLISHABLE_KEY']
}

stripe.api_key = stripe_keys['secret_key']

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)

app.config['BASIC_AUTH_USERNAME'] = 'admin'
app.config['BASIC_AUTH_PASSWORD'] = 'admin'

basic_auth = BasicAuth(app)

from app import views, models
from app.models import User, Challenge, Address, Order, Product, UserHasUser

class ModelView(sqla.ModelView):
    def is_accessible(self):
        if not basic_auth.authenticate():
            raise AuthException('Not authenticated.')
        else:
            return True

    def inaccessible_callback(self, name, **kwargs):
        return redirect(basic_auth.challenge())


from werkzeug.exceptions import HTTPException

class AuthException(HTTPException):
    def __init__(self, message):
        super(AuthException, self).__init__(message, Response(
            "You could not be authenticated. Please refresh the page.", 401,
            {'WWW-Authenticate': 'Basic realm="Login Required"'}
        ))

admin = Admin(app, name='Admin Page')

#With extended views forigen and primary keys will be visible in adminpage
class ExtendedView(ModelView):
    column_display_pk = True # optional, but I like to see the IDs in the list
    column_hide_backrefs = False





login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view =  "login"

@login_manager.user_loader
def load_user(userid):
    return User.query.filter(User.id==userid).first()


# Added all the tables currently in the models/app.db database. Run db_create.py if it doesn't exist.

admin.add_view(ExtendedView(User, db.session))
admin.add_view(ExtendedView(Challenge, db.session))
admin.add_view(ExtendedView(Order, db.session))
admin.add_view(ExtendedView(Product, db.session))
admin.add_view(ExtendedView(UserHasUser, db.session))
admin.add_view(ExtendedView(Address, db.session))
