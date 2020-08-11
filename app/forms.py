from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from flask_uploads import UploadSet, IMAGES
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, Length
from app.models import User, Post

class LoginForm(FlaskForm):
	username = StringField('Username', validators=[DataRequired()])
	password = PasswordField('Password', validators=[DataRequired()])
	remember_me = BooleanField('Remember Me')
	submit_login = SubmitField('Sign In')

class RegistrationForm(FlaskForm):
	username = StringField('Username', validators=[DataRequired()])
	email = StringField('Email', validators=[DataRequired(), Email()])
	password = PasswordField('Password', validators=[DataRequired()])
	password_val = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])
	submit_reg = SubmitField('Register')

	def validate_username(self, username):
		user = User.query.filter_by(username=username.data).first()
		if user is not None:
			raise ValidationError('Please use a different username.')

	def validate_email(self, email):
		user = User.query.filter_by(email=email.data).first()
		if user is not None:
			raise ValidationError('Please use a different email address.')

class UploadForm(FlaskForm):
	images = UploadSet('images', IMAGES)
	filename = StringField('Dish name', validators=[DataRequired(), Length(min=1, max=150)])
	file = FileField('File upload', validators=[FileRequired(), FileAllowed(images, 'Images only')])
	submit = SubmitField('Submit')
	description = StringField('Describe the dish', validators=[DataRequired(), Length(max=500)])
	
	def validate_filename(self, filename):
		post = Post.query.filter_by(title=filename).first()
		if post is not None:
			raise ValidationError('Please use a different dish name.')