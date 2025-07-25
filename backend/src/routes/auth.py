from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt
from ..models.users import create_user, get_user_by_email
from .. import bcrypt
from email_validator import validate_email, EmailNotValidError
from datetime import timedelta

"""
API Authentication routes for JWT-based authentication
Endpoints:
- POST /api/auth/register - User registration
- POST /api/auth/login - User login  
- POST /api/auth/logout - User logout (blacklist token)
- GET /api/auth/me - Get current user info

Features:
- Single 30-day access token
- Token blacklisting for secure logout

TODO:
1. Forgot Password
2. Email Verification  
3. Login with Google
"""

bp = Blueprint('auth', __name__, url_prefix='/api/auth')
# Store for blacklisted tokens (in production, use Redis or database)
blacklisted_tokens = set()

@bp.route('/register', methods=['POST'])
def register():
    """
    Register a new user by taking in name, email, and password as JSON. 
    
    Returns JWT token and user info:
        {
        "access_token": "your_jwt_token",
        "user": {
            "user_id": "user_id",
            "name": "user_name",
            "email": "user_email"
            }
        }
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No JSON data provided'}), 400
        
        name = data.get('name', '').strip() 
        email = data.get('email', '').strip()
        password = data.get('password', '')

        if not name or not email or not password:
            return jsonify({'error': 'Name, email, and password are required'}), 400
        
        # Validation
        if not is_valid_email(email):
            return jsonify({'error': 'Please enter a valid email.'}), 400
            
        # Check if user already exists
        if get_user_by_email(email):
            return jsonify({'error': 'Email already registered. Try signing in.'}), 409
        
        # Create user
        password_hash = bcrypt.generate_password_hash(password).decode('utf-8')
        user_id = create_user(name, email, password_hash)
        
        # Create single long-lived token
        access_token = create_access_token(
            identity=user_id,
            expires_delta=timedelta(days=30)
        )
        
        return jsonify({
            'access_token': access_token,
            'user': {
                'user_id': user_id,
                'name': name,
                'email': email
            }
        }), 201
        
    except Exception as e:
        return jsonify({'error': 'Registration failed', 'details': str(e)}), 500


@bp.route('/login', methods=['POST'])
def login():
    """
    Login user by taking in email and password as JSON.
    
    Returns JWT token and user info:
        {
            "access_token": "your_jwt_token",
            "user": {
                "user_id": "user_id",
                "name": "user_name",
                "email": "user_email"
            }
        }
    """
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No JSON data provided.'}), 400
            
        email = data.get('email', '').strip()
        password = data.get('password', '')
        
        # Validation
        if not email or not password:
            return jsonify({'error': 'Email and password are required.'}), 400
        
        if not is_valid_email(email):
            return jsonify({'error': 'Please enter a valid email.'}), 400
        
        # Find user and verify password
        user = get_user_by_email(email)
        if not user or not bcrypt.check_password_hash(user["password_hash"], password):
            return jsonify({'error': 'Invalid email or password. Please try again.'}), 401
        
        # Create single long-lived token
        access_token = create_access_token(
            identity=user["user_id"],
            expires_delta=timedelta(days=30)
        )
        
        return jsonify({
            'access_token': access_token,
            'user': {
                'user_id': user["user_id"],
                'name': user["name"],
                'email': user["email"],
            }
        }), 200
        
    except Exception as e:
        return jsonify({'error': 'Login failed', 'details': str(e)}), 500


@bp.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    """Logout user by blacklisting the current token."""
    try:
        # Get the unique identifier of the current JWT
        jti = get_jwt()['jti']
        
        # Add token to blacklist
        blacklisted_tokens.add(jti)
        
        return jsonify({'message': 'Successfully logged out'}), 200
        
    except Exception as e:
        return jsonify({'error': 'Logout failed', 'details': str(e)}), 500


# HELPERS
def is_valid_email(email):
    """Check if the email is valid."""
    try:
        validate_email(email)
        return True
    except EmailNotValidError:
        return False

