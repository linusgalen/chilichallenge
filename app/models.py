from app import db



"""
This file has been automatically generated with workbench_alchemy v0.2.3
For more details please check here:
https://github.com/PiTiLeZarD/workbench_alchemy
"""

class User(db.Model):
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)  # pylint: disable=invalid-name
    email = db.Column(db.String(45), unique=True, nullable=False)
    password = db.Column(db.String(45), nullable=False)
    username = db.Column(db.String(45))
    address_id = db.Column(
        db.Integer, db.ForeignKey('address.id', onupdate="CASCADE", ondelete="CASCADE")
    )
    address = db.relationship('Address', backref=db.backref('children', lazy='dynamic'))



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

    #addres = relationship("Addre", foreign_keys=[address_id], backref="user")

    def __repr__(self):
        return self.__str__()

    def __repr__(self):
        return '<User %r>' % (self.username)


class Product(db.Model):

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)  # pylint: disable=invalid-name
    name = db.Column(db.String(45))
    description = db.Column(db.String(200))
    imgurl = db.Column(db.String(45))
    price = db.Column(db.String(45))

    def __repr__(self):
        return str(self.id)



class Order(db.Model):
    id = db.Column(db.Integer, autoincrement=False, primary_key=True, nullable=False)  # pylint: disable=invalid-name
    datetime = db.Column(db.DateTime)
    user_id = db.Column(
        db.Integer, db.ForeignKey("user.id", onupdate="CASCADE", ondelete="CASCADE"), autoincrement=False, primary_key=True,
        index=True
    )
    challenge_id = db.Column(
        db.Integer, db.ForeignKey("challenge.id", onupdate="CASCADE", ondelete="CASCADE"), autoincrement=False,
        primary_key=True, index=True
    )

    #challenge = relationship("Challenge", foreign_keys=[challenge_id], backref="order")
    #user = relationship("User", foreign_keys=[user_id], backref="order")

    def __repr__(self):
        return str(self.challenge_id)




class Challenge(db.Model):


    id=db.Column(db.Integer, primary_key=True, autoincrement=True)
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


    user = db.relationship('User', backref=db.backref('challenge', lazy='dynamic'))
    address = db.relationship('Address', backref=db.backref('challenge', lazy='dynamic'))
    product = db.relationship('Product', backref=db.backref('challenge', lazy='dynamic'))



    #addres = relationship("Addre", foreign_keys=[address_id], backref="challenge")
    #user = relationship("User", foreign_keys=[user_id], backref="challenge")
    #product = relationship("Product", foreign_keys=[product_id], backref="challenge")

    def __repr__(self):
        return str(self.id)



class UserHasUser(db.Model):

    user_id1 = db.Column(
        db.Integer, db.ForeignKey("user.id", onupdate="CASCADE", ondelete="CASCADE"), autoincrement=False, index=True,
        primary_key=True, nullable=False
    )
    user_id2 = db.Column(
        db.Integer, db.ForeignKey("user.id", onupdate="CASCADE", ondelete="CASCADE"), autoincrement=False, index=True,
        primary_key=True, nullable=False
    )

    #user = relationship("User", foreign_keys=[user_id1], backref="userHasUser")
    #user = relationship("User", foreign_keys=[user_id2], backref="userHasUser")

    def __repr__(self):
        return '1:'+str(self.user_id1)+'2:'+str(self.user_id2)





class Address(db.Model):

    id = db.Column(db.Integer, primary_key=True)  # pylint: disable=invalid-name
    first_name = db.Column(db.String(45))
    last_name = db.Column(db.String(45))
    address = db.Column(db.String(45))
    zip = db.Column(db.Integer)
    city = db.Column(db.String(45))
    email = db.Column(db.String(45))

    def __repr__(self):
        return str(self.id)




