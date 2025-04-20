from flask import Blueprint, render_template, redirect, url_for, flash, session, request
from flask_login import login_user, logout_user, login_required
from study_smart import db, bcrypt
from study_smart.models import User
from study_smart.forms import SignupForm, LoginForm

auth = Blueprint('auth', __name__)

@auth.route('/auth/signup', methods=['GET', 'POST'])
def signup():
    form = SignupForm()
    if form.validate_on_submit():
        try:
            hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
            user = User(first_name=form.first_name.data, last_name=form.last_name.data, 
                        email=form.email.data, password_hash=hashed_password)
            db.session.add(user)
            db.session.commit()
            flash('Account created successfully! Please log in.', 'success')
            return redirect(url_for('auth.login'))
        except Exception as e:
            db.session.rollback()
            flash('An error occurred while creating your account.', 'error')
    return render_template('signup.html', form=form)

@auth.route('/auth/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data

        user = User.query.filter_by(email=email).first()
        if user and bcrypt.check_password_hash(user.password_hash, password):
            login_user(user, remember=True)
            flash('Logged in successfully!', 'success')
            return redirect(url_for('views.dashboard'))
        else:
            flash('Invalid email or password.', 'error')

    return render_template('login.html', form=form)

@auth.route('/logout')
@login_required
def logout():
    session.clear()  # This will clear all session data, including flash messages
    logout_user()
    flash('You have been logged out successfully.', 'success')
    return redirect(url_for('auth.login'))
