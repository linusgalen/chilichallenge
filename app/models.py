from app import db

# At first it looked better to do the "declarative mapping" according to alchemy
# tutorial (then we can skip db. all the time but that needs some fixing in
# the other files so right now it's back to normal.
#

# declare mappings as in http://docs.sqlalchemy.org/en/latest/orm/tutorial.html
#from sqlalchemy.ext.declarative import declarative_base
#from sqlalchemy import Column, Integer, String, ForeignKey
#from sqlalchemy.orm import relationship
#from sqlalchemy.types import DateTime

#Base = declarative_base()

"""
This file has been automatically generated with workbench_alchemy v0.2.3
For more details please check here:
https://github.com/PiTiLeZarD/workbench_alchemy
"""

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)  # pylint: disable=invalid-name
    email = db.Column(db.String(45), unique=True, nullable=False)
    password = db.Column(db.String(45), nullable=False)
    username = db.Column(db.String(45))
    address_id = db.Column(
        db.Integer, db.ForeignKey('address.id', onupdate="CASCADE", ondelete="CASCADE")
    )
    # User-Address One-to-One Relationship
    address = db.relationship('Address', uselist=False, back_populates ='user')
    # adding stuff http://docs.sqlalchemy.org/en/latest/orm/basic_relationships.html
    # User-Challenge One-to-Many Relationship
    challenge = db.relationship('Challenge')
    order = db.relationship("Order", uselist=False, back_populates="user")

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id)  # python 3


    def __repr__(self):
        return self.__str__()

    def __repr__(self):
        return '<User %r>' % (self.username)


class Product(db.Model):
    __tablename__ = 'product'
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)  # pylint: disable=invalid-name
    name = db.Column(db.String(45))
    description = db.Column(db.String(200))
    imgurl = db.Column(db.String(120))
    price = db.Column(db.String(45))

    #One-to-Many relationship
    challenge = db.relationship("Challenge")

    def __repr__(self):
        return str(self.id)
#
#   TODO: The order table is still not working properly.
#   Should have a Many-to-one relationship with user and
#   One-to-one with challenge.

class Order(db.Model):
    __tablename__ = 'order'
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)  # pylint: disable=invalid-name
    datetime = db.Column(db.DateTime)
    user_id = db.Column(
        db.Integer, db.ForeignKey('user.id', onupdate="CASCADE", ondelete="CASCADE"),
    )
    challenge_id = db.Column(
        db.Integer, db.ForeignKey('challenge.id', onupdate="CASCADE", ondelete="CASCADE"),
    )

    challenge = db.relationship("Challenge", back_populates="order")
    user = db.relationship("User", back_populates="order")

    def __repr__(self):
        return str(self.challenge_id)


class Challenge(db.Model):

    __tablename__ = 'challenge'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    message = db.Column(db.String(300))
    datetime = db.Column(db.DateTime)
    product_id = db.Column(
        db.Integer, db.ForeignKey("product.id", onupdate="CASCADE", ondelete="CASCADE")
    )
    user_id = db.Column(
        db.Integer, db.ForeignKey("user.id", onupdate="CASCADE", ondelete="CASCADE")
    )
    address_id = db.Column(
        db.Integer, db.ForeignKey("address.id", onupdate="CASCADE", ondelete="CASCADE")
    )
    challenge_code = db.Column(db.String(10), unique=True)
    answer_message = db.Column(db.String(300))


    challenge_code = db.Column(db.String(10), unique=True)

    address = db.relationship("Address", back_populates="challenge")
    user = db.relationship("User", back_populates="challenge")
    product = db.relationship("Product", back_populates="challenge")
    order = db.relationship("Order")


    def __repr__(self):
        return str(self.id)

# Still not sure about this table below, check out: Many To Many @
# http://docs.sqlalchemy.org/en/latest/orm/basic_relationships.html

class UserHasUser(db.Model):
    __tablename__ = 'user_has_user'

    #id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id1 = db.Column(
        db.Integer, db.ForeignKey("user.id", onupdate="CASCADE", ondelete="CASCADE"), autoincrement=False, index=True,
        primary_key=True, nullable=False
    )
    user_id2 = db.Column(
        db.Integer, db.ForeignKey("user.id", onupdate="CASCADE", ondelete="CASCADE"), autoincrement=False, index=True,
        primary_key=True, nullable=False
    )

    user1 = db.relationship("User",  foreign_keys=[user_id1])
    user2 = db.relationship("User",  foreign_keys=[user_id2])

    def __repr__(self):
        return '1:'+str(self.user_id1)+'2:'+str(self.user_id2)


class Address(db.Model):
    __tablename__ = 'address'
    id = db.Column(db.Integer, primary_key=True)  # pylint: disable=invalid-name
    first_name = db.Column(db.String(45))
    last_name = db.Column(db.String(45))
    address = db.Column(db.String(45))
    zip = db.Column(db.Integer)
    city = db.Column(db.String(45))
    email = db.Column(db.String(45))

    challenge = db.relationship("Challenge")
    user = db.relationship("User", back_populates="address")

    def __repr__(self):
        return str(self.id)
