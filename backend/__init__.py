from flask import Flask
from dotenv import load_dotenv
import os
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_cors import CORS


# Load variables from .env file
load_dotenv()

# Initialize Flask extensions
bcrypt = Bcrypt()
jwt = JWTManager()


def create_app():
    app = Flask(__name__)
    
    # Load configuration from environment
    app.secret_key = os.getenv("SECRET_KEY")
    app.config['JWT_SECRET_KEY'] = os.getenv("JWT_SECRET_KEY")
    
    # Initialize Flask extensions
    bcrypt.init_app(app)
    jwt.init_app(app)
    
    # Configure CORS for API endpoints
    CORS(app, supports_credentials=True)

    # JWT token blacklist checking
    @jwt.token_in_blocklist_loader
    def check_if_token_revoked(jwt_header, jwt_payload):
        from backend.routes.auth import blacklisted_tokens
        jti = jwt_payload['jti']
        return jti in blacklisted_tokens

    # Register Blueprints
    from .routes.auth import bp as auth_bp
    from .routes.search import bp as search_bp
    from .routes.tts import bp as tts_bp
    from .routes.vocab import bp as vocab_bp
    from .routes.placement import bp as placement_bp
    from .routes.practice import bp as practice_bp
    app.register_blueprint(auth_bp)
    app.register_blueprint(search_bp)
    app.register_blueprint(tts_bp)
    app.register_blueprint(vocab_bp)
    app.register_blueprint(placement_bp)
    app.register_blueprint(practice_bp)
    
    return app
