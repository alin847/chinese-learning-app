from backend.models.progress import get_progress, add_time_spent, add_practice_completed
from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity


bp = Blueprint('progress', __name__, url_prefix='/api/progress')

@bp.route('/', methods=['GET'])
@jwt_required()
def get_user_progress():
    """
    Retrieve the progress of the current user.
    Returns a JSON object with counts of words in different states and time spent.
    """
    user_id = get_jwt_identity()
    progress = get_progress(user_id)
    
    return jsonify(progress), 200

@bp.route('/time_spent', methods=['PUT'])
@jwt_required()
def update_time_spent():
    """
    Update the time spent by the user.
    Expects JSON with 'time_spent' field.
    """
    user_id = get_jwt_identity()
    data = request.get_json()

    if not data or 'time_spent' not in data:
        return jsonify({'error': 'Invalid data provided.'}), 400

    time_spent = data['time_spent']
    
    add_time_spent(user_id, time_spent)
    
    return jsonify({'message': 'Time spent updated successfully.'}), 200


@bp.route('/practice_completed', methods=['PUT'])
@jwt_required()
def increment_practice_completed():
    """
    Increment the practice completed count for the user.
    """
    user_id = get_jwt_identity()
    
    add_practice_completed(user_id)
    
    return jsonify({'message': 'Practice completed count incremented successfully.'}), 200