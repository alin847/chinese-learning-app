from flask import Blueprint, render_template, session
from flask_login import login_required, current_user

bp = Blueprint('home', __name__)

@bp.route('/home')
@login_required
def home():
    """Render the home page."""
    return render_template('home.html', user=None)
