from src.models.test_bank import get_random_question
from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from src.models.dictionary import get_word_ids_by_hsk
from src.models.vocab_bank import add_vocab_batch, get_random_vocab
from datetime import date, timedelta
import random


bp = Blueprint('placement', __name__, url_prefix='/api/placement')

@bp.route('/question', methods=['POST'])
@jwt_required()
def placement_question():
    """
    Fetch a random question for the placement test.
    
    Args:
    - level: int, the HSK level of the question (1-6)
    - excluded: list, question IDs to exclude from the selection
    
    Returns a question dictionary with the following structure:
    {
        "question_id": int,  # Question ID
        "text": str,  # Question text
        "answer": str,  # Correct answer
        "options": list  # List of answer options
    }
    """
    data = request.get_json()
    level = data.get('level')
    excluded = data.get('excluded', [])

    if not isinstance(excluded, list):
        return jsonify({'error': 'Excluded must be a list.'}), 400

    question = get_random_question(level, excluded)
    
    if not question:
        return jsonify({'error': 'No question found for the given level.'}), 404
    
    return jsonify(question), 200
    

@bp.route('/add-initial-vocab', methods=['POST'])
@jwt_required()
def add_initial_vocab():
    """
    Add initial vocabulary words to the user's vocabulary bank based on their HSK level.

    Args:
    - level: int, the HSK level of the user (1-6)
    """
    data = request.get_json()
    level = data.get('level', 1)
    user_id = get_jwt_identity()

    # Add all HSK level - 1 vocabulary words to the user's vocabulary bank
    repetition = 1
    interval = 0
    for i in range(level - 1, 0, -1):
        try:
            # get all vocabulary words for the given HSK level
            simplified_ids = get_word_ids_by_hsk(i)
            repetitions = [repetition] * len(simplified_ids)
            intervals = [interval] * len(simplified_ids)
            next_reviews = [date.today() + timedelta(days=random.randrange(31)) 
                            for _ in range(len(simplified_ids))]
            add_vocab_batch(user_id, simplified_ids, repetitions, intervals, next_reviews)
            repetition += 1
            interval += 5
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    # Add 20 random words to the user's vocabulary bank
    random_vocab = get_random_vocab(user_id, 20)
    simplified_ids = [word['simplified_id'] for word in random_vocab]
    repetitions = [0] * len(simplified_ids)
    intervals = [0] * len(simplified_ids)
    next_reviews = [date.today()] * len(simplified_ids)
    add_vocab_batch(user_id, simplified_ids, repetitions, intervals, next_reviews)
    return jsonify({'message': 'Initial vocabulary added successfully.'}), 200
