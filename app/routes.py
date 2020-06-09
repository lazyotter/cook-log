from flask import render_template, flash, redirect
from app import app
from app.forms import LoginForm

@app.route('/', methods = ['GET', 'POST'])
@app.route('/index', methods = ['GET', 'POST'])
def index():
	form = LoginForm()
	if form.validate_on_submit():
		flash('Login requested for user {}, remember_me={}'.format(
			form.username.data, form.remember_me.data))
		return redirect('/index')
	return render_template('index.html', form=form)

'''@app.route('/login')
def login():
	form = LoginForm()
	return render_template('login.html', title='Sign In', form=form)
'''