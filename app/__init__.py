from flask import Flask, Response
from flask_sqlalchemy import SQLAlchemy
from flask_basicauth import BasicAuth
from flask_admin import Admin
from flask_admin.contrib import sqla

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)

app.config['BASIC_AUTH_USERNAME'] = 'admin'
app.config['BASIC_AUTH_PASSWORD'] = 'admin'

basic_auth = BasicAuth(app)

from app import views, models
## from models import User, Book, Contactpost

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
##admin.add_view(ModelView(User, db.session))
##admin.add_view(ModelView(Book, db.session))
##admin.add_view(ModelView(Contactpost, db.session))
