from flask import Flask
from dotenv import load_dotenv
import os
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from app.models.users import get_user_by_id

# Load variables from .env file
load_dotenv()

# Initialize Flask extensions
bcrypt = Bcrypt()
login_manager = LoginManager()


def create_app():
    app = Flask(__name__)
    
    # Load secret key from environment
    app.secret_key = os.getenv("SECRET_KEY")
    
    # Initialize Flask extensions
    bcrypt.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'  # where to redirect if not logged in (change later)

    # Register Blueprints
    from .routes.auth import bp as auth_bp
    from .routes.home import bp as home_bp
    app.register_blueprint(auth_bp)
    app.register_blueprint(home_bp)
    return app

@login_manager.user_loader
def load_user(user_id):
    return get_user_by_id(user_id)