from app import db,app
from flask_login import UserMixin



class User(db.Model, UserMixin):
    __tablename__ = 'customer'
    id = db.Column(db.Integer,primary_key=True)
    f_name = db.Column(db.String(20), nullable=False)
    l_name = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(30), unique=True, nullable=False)
    password = db.Column(db.String(500))

    def add_sale(self):
        db.session.add(self)
        db.session.commit()