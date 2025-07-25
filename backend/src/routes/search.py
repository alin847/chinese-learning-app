from flask import Blueprint, request, jsonify
from ..models.dictionary import get_search_results
from ..models.vocab_bank import get_all_vocab, get_random_vocab
from flask_jwt_extended import jwt_required, get_jwt_identity

bp = Blueprint('search', __name__, url_prefix='/api')  

# Perhaps caching???
@bp.route('/search/<search_type>/<query>', methods=['GET'])
@jwt_required()
def search_query(search_type, query):
    """
    Search for a query in the dictionary.
    
    Args:
    - search_type: str, the type of search (simplified, pinyin, definitions, id)
    - query: str, the search query

    Returns a list of search results with the following structure:
    [
        {
            "simplified_id": int,  # Unique identifier for the word
            "simplified": str,  # The simplified Chinese word
            "pinyin": str,  # Pinyin representation of the word
            "definitions": list,  # List of definitions for the word
            "sentences": list,  # List of sentences using the word
            "is_added": bool  # Whether the word is already in the user's vocabulary bank
        },
        ...
    ]
    """
    KEY = {"simplified": "simplified",
           "pinyin": "pinyin_normalized",
           "definitions": "definitions",
           "id": "simplified_id"}
    user_id = get_jwt_identity()

    results = get_search_results(KEY[search_type], query)
    all_vocab = get_all_vocab(user_id)
    # Convert all_vocab to a set for faster lookup
    all_vocab_set = {vocab["simplified_id"] for vocab in all_vocab}

    for result in results:
        # Fetch is_added status
        result["is_added"] = True if result["simplified_id"] in all_vocab_set else False

    return jsonify(results), 200

@bp.route('/search/recommended', methods=['GET'])
@jwt_required()
def search_recommended():
    """
    Get a list of recommended words for the user to add to vocabulary bank.

    Returns a list of recommended words with the following structure:
    [
        {
            "simplified_id": int,  # Unique identifier for the word
            "simplified": str,  # The simplified Chinese word
            "pinyin": str,  # Pinyin representation of the word
            "definitions": list,  # List of definitions for the word    
            "sentences": list,  # List of sentences using the word
            "is_added": bool  # Whether the word is already in the user's vocabulary bank
        },
        ...
    ]
    """
    user_id = get_jwt_identity()
    results = get_random_vocab(user_id, 30)
    for result in results:
        result["is_added"] = False
    return jsonify(results), 200


@bp.route('/search', methods=["GET"])
@jwt_required()
def search():
    """
    Search for a word in the dictionary. The search 'type' can be:
    - simplified
    - pinyin
    - definitions
    Expects: /search?type=xxx

    Returns a list of search results with the following structure:
    [
        {
            "simplified_id": int,  # Unique identifier for the word
            "simplified": str,  # The simplified Chinese word
            "pinyin": str,  # Pinyin representation of the word
            "definitions": list,  # List of definitions for the word
            "sentences": list  # List of sentences using the word
        },
        ...
    ]
    """
    # Extract the search parameters
    simplified = request.args.get('simplified', '').strip()
    pinyin = request.args.get('pinyin', '').strip()
    definition = request.args.get('definitions', '').strip()

    # check if only one search parameter is provided
    if sum([bool(simplified), bool(pinyin), bool(definition)]) != 1:
        return jsonify({'error': 'Please provide exactly one valid search field.'}), 400

    try:
        if simplified:
            results = get_search_results('simplified', simplified)
        elif pinyin:
            results = get_search_results('pinyin_normalized', pinyin)
        else:
            results = get_search_results('definitions', definition)

        return jsonify(results), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
