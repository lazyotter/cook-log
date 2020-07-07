from flask import render_template, flash, redirect, url_for
from app import app
from app.forms import LoginForm, RegistrationForm
from flask_login import current_user, login_user, logout_user
from app.models import User

@app.route('/', methods = ['GET', 'POST'])
@app.route('/index', methods = ['GET', 'POST'])
def index():
	form = LoginForm()
	reg_form = RegistrationForm()
	if current_user.is_authenticated:
		return render_template('index.html', title='Home Page')
	if form.validate_on_submit():
		user = User.query.filter_by(username=form.username.data).first()
		if user is None or not user.check_password(form.password.data):
			flash('Invalid username or password')
			return redirect('/index')
		login_user(user, remember=form.remember_me.data)
		return redirect(url_for('index'))
	if reg_form.validate_on_submit():
		user = User(username=reg_form.username.data, email=reg_form.email.data)
		user.set_password(reg_form.password.data)
		db.session.add(user)
		db.session.commit()
		flash('YOU REGISTERED DUMB SHIT')
		return redirect(url_for('index'))
	return render_template('index.html', form=form, reg_form=reg_form, title='Home Page')

@app.route('/logout')
def logout():
	logout_user()
	return redirect(url_for('index'))
'''@app.route('/login')
def login():
	form = LoginForm()
	return render_template('login.html', title='Sign In', form=form)
'''