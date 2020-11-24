from flask_wtf import FlaskForm
from wtforms import PasswordField, BooleanField, SubmitField, StringField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from wtforms.fields.html5 import EmailField
from app.models import User

class LoginForm(FlaskForm):
	email = EmailField('Email', validators = [DataRequired(message='An email is required.'), Email()])
	password = PasswordField('Password', validators = [DataRequired(message='A password is required.')])
	remember_me = BooleanField('Remember me')
	submit = SubmitField('Sign In')
	
class RegistrationForm(FlaskForm):
	email = EmailField('Email', validators = [DataRequired(message='An email is required.'), Email()])
	password = PasswordField('Password', validators = [DataRequired(message='A password is required.')])
	password2 = PasswordField('Repeat password', validators = [DataRequired(), EqualTo('password', message = 'Passwords mismatch.')])
	submit = SubmitField('Sign up')
	
	def validate_email(self, email):
		user = User.query.filter_by(email=self.email.data).first()
		if user is not None:
			raise ValidationError('That email address is already in use.')
			
class ResetPasswordRequestForm(FlaskForm):
	email = StringField('Email', validators=[DataRequired(message='An email is required.'), Email()])
	submit = SubmitField('Reset')
	
class ResetPasswordForm(FlaskForm):
	password = PasswordField('Password', validators = [DataRequired(message='A password is required.')])
	password2 = PasswordField('Repeat password', validators = [DataRequired(), EqualTo('password', message = 'Passwords mismatch.')])
	submit = SubmitField('Change')