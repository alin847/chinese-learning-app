from flask import Blueprint, render_template, redirect
from flask_login import current_user

bp = Blueprint('index', __name__)

@bp.route('/')
def index():
    """Render the main page."""
    if current_user.is_authenticated:
        return redirect('/home')  # Redirect to home if user is authenticated
    return render_template('index.html', user=None)
