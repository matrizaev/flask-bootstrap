from flask import render_template, redirect, url_for, flash, request
from app import db
from app.auth import bp
from flask_login import login_user, logout_user, current_user
from werkzeug.urls import url_parse
from app.auth.forms import LoginForm, RegistrationForm, ResetPasswordRequestForm, ResetPasswordForm
from app.models import User
from app.auth.email import SendPasswordResetEmail
from flask import current_app

@bp.route('/login/', methods = ['GET', 'POST'])
def PerformLogin():
	if current_user.is_authenticated:
		return redirect(url_for('main.ShowIndex'))
	form = LoginForm()
	if form.validate_on_submit():
		email = form.email.data.lower()
		user = User.query.filter_by(email = email).first()
		if user is None or not user.CheckPassword(form.password.data):
			flash('The email and the password are incorrect.')
			return redirect(url_for('auth.PerformLogin'))
		login_user(user, remember=form.remember_me.data)
		current_app.logger.info('{} logged'.format(user.email))
		return redirect(url_for('main.ShowIndex'))
	return render_template ('auth/login.html', form = form)

@bp.route('/register/', methods = ['GET', 'POST'])
def PerformRegistration():
	if current_user.is_authenticated:
		return redirect(url_for('main.ShowIndex'))
	form = RegistrationForm()
	if form.validate_on_submit():
		email = form.email.data.lower()
		user = User(email = email)
		user.SetPassword(form.password.data)
		db.session.add(user)
		db.session.commit()
		flash ('You can now sign in.')
		current_app.logger.info('{} registered'.format(user.email))
		return redirect(url_for('auth.PerformLogin'))
	return render_template ('auth/register.html', form = form)

@bp.route('/logout/')
def PerformLogout():
	logout_user()
	return redirect(url_for('auth.PerformLogin'))
	
@bp.route('/request/', methods=['GET', 'POST'])
def RequestPaswordReset():
	if current_user.is_authenticated:
		return redirect(url_for('main.ShowIndex'))
	form = ResetPasswordRequestForm()
	if form.validate_on_submit():
		user = User.query.filter_by(email=form.email.data).first()
		if user:
			SendPasswordResetEmail(user)
			flash('The password reset email has been sent to you.')
			return redirect(url_for('auth.PerformLogin'))
		else:
			flash('The user has not been found.')
	return render_template('auth/request.html', form = form)
	
@bp.route('/reset/<token>', methods=['GET', 'POST'])
def ResetPassword(token):
	if current_user.is_authenticated:
		return redirect(url_for('main.ShowIndex'))
	user = User.VerifyPasswordResetToken(token)
	if not user:
		return redirect(url_for('main.ShowIndex'))
	form = ResetPasswordForm()
	if form.validate_on_submit():
		user.SetPassword(form.password.data)
		db.session.commit()
		flash('Your password has been changed.')
		return redirect(url_for('auth.PerformLogin'))
	return render_template('auth/reset.html', form=form)