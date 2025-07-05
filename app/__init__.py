from flask import Flask
from dotenv import load_dotenv
import os

# Load variables from .env file
load_dotenv()

def create_app():
    app = Flask(__name__)
    
    # Load secret key from environment
    app.secret_key = os.getenv("SECRET_KEY", "default-secret-key")

    # Register Blueprints here if you have them
    # from .routes.auth import bp as auth_bp
    # app.register_blueprint(auth_bp)

    return app