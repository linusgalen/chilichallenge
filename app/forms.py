from flask_wtf import Form
from wtforms import StringField, PasswordField, BooleanField, IntegerField
from wtforms.validators import DataRequired, Email

class UserForm(Form):
    name = StringField('Name', validators=[DataRequired()])
    username= StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('remember_me', default=False)
    address = StringField('Address', validators=[DataRequired()])
    zipcode    = IntegerField('Zipcode', validators=[DataRequired()])
    city = StringField('City', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired()])

class AddressForm(Form):
    first_name = StringField('First name', validators=[DataRequired()])
    last_name = StringField('Last name', validators=[DataRequired()])
    address = StringField('Address', validators=[DataRequired()])
    zipcode = IntegerField('Zipcode', validators=[DataRequired()])
    city = StringField('City', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    product_id = IntegerField('Product id')


