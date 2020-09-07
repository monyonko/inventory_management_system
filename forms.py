from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField, DateField, IntegerField
from wtforms import validators
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from admin import Administration
from employee import Employee
from customer import User
import email_validator


class RegistrationForm(FlaskForm):
    f_name = StringField('f_name', validators=[DataRequired(), 
    Length(min=2, max=20)])
    l_name = StringField('l_name', validators=[DataRequired(), 
    Length(min=2, max=20)])
    username = StringField('Username', validators=[DataRequired(), 
    Length(min=4, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password =PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(),EqualTo('password')])
    submit= SubmitField('Sign Up')

    def validate_email(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError("Username exists. Please choose another one")

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError("Email exists. Please choose another one")

class RegistrationForm1(FlaskForm):
    f_name = StringField('f_name', validators=[DataRequired(), 
    Length(min=2, max=20)])
    l_name = StringField('l_name', validators=[DataRequired(), 
    Length(min=2, max=20)])
    username = StringField('Username', validators=[DataRequired(), 
    Length(min=4, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    department = StringField('Department', validators=[DataRequired()])
    date_employed = DateField('Start Date', format='%m/%d/%Y', validators=(validators.Optional(),))
    password =PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(),EqualTo('password')])
    submit= SubmitField('Submit')

    
    def validate_email(self, username):
        user = Administration.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError("Username exists. Please choose another one")
    def validate_email(self, email):
        user = Administration.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError("Email exists. Please choose another one")

class RegistrationForm2(FlaskForm):
    f_name = StringField('f_name', validators=[DataRequired(), 
    Length(min=2, max=20)])
    l_name = StringField('l_name', validators=[DataRequired(), 
    Length(min=2, max=20)])
    username = StringField('Username', validators=[DataRequired(), 
    Length(min=4, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    department = StringField('Department', validators=[DataRequired()])
    education_level = StringField('Education Level', validators=[DataRequired()])
    managed_by = IntegerField('Manager ID')
    salary = IntegerField('Salary', validators=[DataRequired()])
    date_employed = DateField('Start Date', format='%m/%d/%Y', validators=(validators.Optional(),))
    password =PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(),EqualTo('password')])
    submit= SubmitField('Submit')

    
    def validate_email(self, username):
        user = Employee.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError("Username exists. Please choose another one")

    def validate_email(self, email):
        user = Employee.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError("Email exists. Please choose another one")

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), 
    Length(min=4, max=20)])
    password =PasswordField('Password', validators=[DataRequired()])
    remember=BooleanField('Remember Me')
    submit= SubmitField('Login')

