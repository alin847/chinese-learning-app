from src.models.vocab_bank import add_vocab, update_vocab, get_vocab, get_all_vocab, delete_vocab
from src.models.dictionary import get_word_by_id
from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity

bp = Blueprint('vocab', __name__, url_prefix='/api/vocab')

@bp.route('/all', methods=['GET'])
@jwt_required()
def vocabulary():
    """
    Retrieve all vocabulary words for the user, categorized into learning, reviewing, and mastered.
    Each category contains a list of vocabulary words with the following fields:
    - simplified_id: int,  # Unique identifier for the word
    - simplified: str,  # The simplified Chinese word
    - pinyin: str,  # Pinyin representation of the word
    - definitions: list,  # List of definitions for the word
    - sentences: list  # List of example sentences using the word
    """
    user_id = get_jwt_identity()
    vocab = get_all_vocab(user_id)
    simplified_ids = [v['simplified_id'] for v in vocab]
    words = get_word_by_id(simplified_ids)

    learning_vocab = []
    reviewing_vocab = []
    mastered_vocab = []
    for i, v in enumerate(vocab):
        if v['repetitions'] < 2:
            learning_vocab.append(words[i])
        elif 2 <= v['repetitions'] < 4:
            reviewing_vocab.append(words[i])
        else:
            mastered_vocab.append(words[i])


    return jsonify({"learning_vocab": learning_vocab,
                    "reviewing_vocab": reviewing_vocab, 
                    "mastered_vocab": mastered_vocab}), 200


@bp.route('/', methods=['POST', 'GET', 'PUT', 'DELETE'])
@jwt_required()
def vocab_api():
    """
    Handle vocabulary operations: add, update, delete, and retrieve vocabulary words.

    GET: Retrieve a vocabulary word by 'simplified_id'.
    POST: Add a new vocabulary word by 'simplified_id'.
    PUT: Update an existing vocabulary word with 'simplified_id', 'repetitions', 'interval', and 'ease_factor'.
    DELETE: Delete a vocabulary word by 'simplified_id'.
    """
    user_id = get_jwt_identity()

    # Get vocabulary word by simplified_id
    if request.method == 'GET':
        data = request.args
        simplified_id = data.get('simplified_id', '')
        try:
            vocab = get_vocab(user_id, simplified_id)
            return jsonify(vocab), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500
        
    data = request.get_json()
    if not data or 'simplified_id' not in data:
        return jsonify({'error': 'Invalid data provided.'}), 400

    simplified_id = data['simplified_id']

    if request.method == 'POST':
        # Add new vocabulary word
        try:
            if add_vocab(user_id, simplified_id):
                return jsonify({'message': 'Vocabulary word added successfully.'}), 201
            else:
                return jsonify({'error': 'Failed to add vocabulary word.'}), 500
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    elif request.method == 'PUT':
        # Update existing vocabulary word
        if 'repetitions' not in data or 'interval' not in data or 'ease_factor' not in data:
            return jsonify({'error': 'Invalid data for update.'}), 400
        
        vocab = {
            'simplified_id': simplified_id,
            'repetitions': data['repetitions'],
            'interval': data['interval'],
            'ease_factor': data['ease_factor']
        }
        
        try:
            if update_vocab(user_id, vocab):
                return jsonify({'message': 'Vocabulary word updated successfully.'}), 200
            else:
                return jsonify({'error': 'Failed to update vocabulary word.'}), 500
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    elif request.method == 'DELETE':
        # Delete vocabulary word
        try:
            if delete_vocab(user_id, simplified_id):
                return jsonify({'message': 'Vocabulary word deleted successfully.'}), 200
            else:
                return jsonify({'error': 'Failed to delete vocabulary word.'}), 500
        except Exception as e:
            return jsonify({'error': str(e)}), 500
        
    