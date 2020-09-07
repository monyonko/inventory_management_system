from app import db,app
from flask_login import UserMixin
from datetime import datetime
from sqlalchemy.sql import expression





class Employee(db.Model, UserMixin):
    __tablename__ = 'employees'
    id = db.Column(db.Integer,primary_key=True)
    f_name = db.Column(db.String(20), nullable=False)
    l_name = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(30), nullable=False, unique=True)
    department = db.Column(db.String(30), nullable=False, unique=True)
    education_level =  db.Column(db.String(20), unique=False, nullable=False)
    managed_by = db.Column(db.Integer, db.ForeignKey('administration.id'))
    salary = db.Column(db.Integer, nullable=False)
    date_employed = db.Column(db.DateTime, default=datetime.utcnow)
    password = db.Column(db.String(500), nullable=False)

    def add_sale(self):
        db.session.add(self)
        db.session.commit()