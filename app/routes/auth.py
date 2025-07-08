from flask import Blueprint, request, redirect, render_template, flash, session
from app.models.users import create_user, get_user_by_email
from app import bcrypt
from email_validator import validate_email, EmailNotValidError
import re
from flask_login import login_user, logout_user, login_required, current_user
"""
Implement later:
1. Forgot Password
2. Email Verification
3. Login with Google
"""

bp = Blueprint('auth', __name__)

@bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        
        if not is_valid_email(email):
            error_message = "Invalid email. Please enter a valid email address."
            return render_template('register.html', error_message=error_message)
        if get_user_by_email(email):
            error_message = "Email already registered. Please sign in."
            return render_template('register.html', error_message=error_message)
        
        password = request.form['password']
        password_hash = bcrypt.generate_password_hash(password).decode('utf-8')
        create_user(email, password_hash)
        return redirect('/')

    return render_template('register.html')


@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user = get_user_by_email(email)
        if not user or not bcrypt.check_password_hash(user.password_hash, password):
            error_message = "Invalid email or password. Please try again or create an account."
            return render_template('login.html', error_message=error_message)

        login_user(user)

        return redirect('/') # change this redirect to a dashboard or home page

    return render_template('login.html')


@bp.route('/logout')
@login_required
def logout():
    """Log out the user."""
    logout_user()
    flash('Logged out successfully.')
    return redirect('/login')


# HELPERS
def is_valid_email(email):
    """Check if the email is valid."""
    try:
        valid = validate_email(email)
        return valid.email
    except EmailNotValidError:
        return None

