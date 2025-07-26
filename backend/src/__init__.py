from flask import Flask
from dotenv import load_dotenv
import os
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_cors import CORS
import base64
from google.cloud import texttospeech
from google.cloud import speech
from src.db import get_conn, put_conn

# Load variables from .env file
load_dotenv()

# Initialize Flask extensions
bcrypt = Bcrypt()
jwt = JWTManager()

# Initialize google cloud tts/stt client
key_b64 = os.getenv("GOOGLE_APPLICATION_CREDENTIALS_B64")
if key_b64 and not os.path.exists("google_credentials.json"):
    with open("google_credentials.json", "wb") as f:
        f.write(base64.b64decode(key_b64))
tts_client = texttospeech.TextToSpeechClient.from_service_account_json("google_credentials.json")
stt_client = speech.SpeechClient.from_service_account_json("google_credentials.json")

def create_app():
    app = Flask(__name__)
    
    # Load configuration from environment
    app.secret_key = os.getenv("SECRET_KEY")
    app.config['JWT_SECRET_KEY'] = os.getenv("JWT_SECRET_KEY")
    
    # Initialize Flask extensions
    bcrypt.init_app(app)
    jwt.init_app(app)
    
    # Configure CORS for API endpoints
    CORS(app, origins=["http://localhost:5173", os.getenv('FRONTEND_URL')], supports_credentials=True)

    # JWT token blacklist checking
    @jwt.token_in_blocklist_loader
    def check_if_token_revoked(jwt_header, jwt_payload):
        jti = jwt_payload['jti']
        conn = get_conn()
        try:
            with conn.cursor() as cursor:
                cursor.execute(
                    "SELECT 1 FROM jwt_blacklist WHERE jti = %s",
                    (jti,)
                )
                result = cursor.fetchone()
                return result is not None  # True means it's blacklisted
        finally:
            put_conn(conn)

    # Register Blueprints
    from .routes.auth import bp as auth_bp
    from .routes.search import bp as search_bp
    from .routes.tts import bp as tts_bp
    from .routes.vocab import bp as vocab_bp
    from .routes.placement import bp as placement_bp
    from .routes.practice import bp as practice_bp
    from .routes.progress import bp as progress_bp
    app.register_blueprint(auth_bp)
    app.register_blueprint(search_bp)
    app.register_blueprint(tts_bp)
    app.register_blueprint(vocab_bp)
    app.register_blueprint(placement_bp)
    app.register_blueprint(practice_bp)
    app.register_blueprint(progress_bp)
    
    return app
