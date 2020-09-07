from app import db,app
from flask_login import UserMixin
from datetime import datetime




class Administration(db.Model, UserMixin):
    __tablename__ = 'administration'
    id = db.Column(db.Integer,primary_key=True)
    f_name = db.Column(db.String(20), nullable=False)
    l_name = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(20), nullable=False, unique=True)
    department = db.Column(db.String(20), unique=True, nullable=False)
    date_employed = db.Column(db.DateTime, default=datetime.utcnow)
    password = db.Column(db.String(500), nullable=False)


    employee = db.relationship('Employee',backref='employees',lazy=True)


    def add_sale(self):
        db.session.add(self)
        db.session.commit()