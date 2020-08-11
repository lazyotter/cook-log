from flask import render_template, flash, redirect, url_for
from app import app, db
from app.forms import LoginForm, RegistrationForm, UploadForm
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.utils import secure_filename
from app.models import User, Post

@app.route('/', methods = ['GET', 'POST'])
@app.route('/index', methods = ['GET', 'POST'])
def index():
	login_form = LoginForm()
	reg_form = RegistrationForm()

	# Check if already logged in
	if current_user.is_authenticated:
		return redirect(url_for('user', username=current_user.username))

	# If submitting login form, validate form
	if login_form.submit_login.data and login_form.validate():
		user = User.query.filter_by(username=login_form.username.data).first()
		# If user does not exist or password doesnt work
		if user is None or not user.check_password(login_form.password.data):
			flash('Invalid username or password')
			return redirect(url_for('index'))
		# Login existing user
		login_user(user, remember=login_form.remember_me.data)
		return redirect(url_for('user', username=current_user.username)) 
	# If submitting registration form, check that validators and if data is there
	if reg_form.submit_reg.data and reg_form.validate():
		user = User(username=reg_form.username.data, email=reg_form.email.data)
		user.set_password(reg_form.password.data)
		db.session.add(user)
		db.session.commit()
		flash('YOU REGISTERED DUMB SHIT')
		return redirect(url_for('index'))
	return render_template('index.html', login_form=login_form, reg_form=reg_form, title='Home Page')

@app.route('/logout')
def logout():
	logout_user()
	return redirect(url_for('index'))

@app.route('/user/<username>')
@login_required
def user(username):
	user = User.query.filter_by(username=username).first_or_404()
	return render_template('home.html', user=user)

@app.route('/user/<username>/upload', methods = ['GET', 'POST'])
@login_required
def upload(username):
	upload_form = UploadForm()
	if upload_form.validate_on_submit():
		# Get username
		user = User.query.filter_by(username=username).first_or_404()

		# Get image data and save to local computer
		data = upload_form.file.data
		filename = secure_filename(upload_form.filename)
		data.save(os.path.join(app.instance_path, 'app/static/images/', user, 
			'/', 'filename'))

		# Save post to database
		post = Post(title=upload_form.name, file_path=filename)
		db.session.add(post)
		db.session.commit()
		flash('Upload successful')

		return redirect(url_for('user'), user=user)
	return render_template('upload.html', upload_form=upload_form, title='Upload foodies')

