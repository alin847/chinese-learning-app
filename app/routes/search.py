from flask import Blueprint, request, jsonify
from app.models.dictionary import get_search_results
from app.models.vocab_bank import get_vocab, get_all_vocab, add_vocab, update_vocab, get_random_vocab
from flask_jwt_extended import jwt_required

bp = Blueprint('search', __name__, url_prefix='/api')  

# Perhaps caching???
@bp.route('/search/<search_type>/<query>', methods=['POST'])
@jwt_required()
def search_query(search_type, query):
    """Search for a query in the dictionary and render results."""
    KEY = {"simplified": "simplified",
           "pinyin": "pinyin_normalized",
           "definitions": "definitions",
           "id": "id"}
    data = request.get_json()
    user = data.get('user', '')

    results = get_search_results(KEY[search_type], query)
    all_vocab = get_all_vocab(user['id'])
    # Convert all_vocab to a set for faster lookup
    all_vocab_set = {vocab["simplified_id"] for vocab in all_vocab}

    for result in results:
        # Fetch is_added status
        result["is_added"] = True if result["id"] in all_vocab_set else False

    return jsonify(results)

@bp.route('/search/recommended', methods=['POST'])
@jwt_required()
def search_recommended():
    data = request.get_json()
    user = data.get('user', '')
    results = get_random_vocab(user["id"], 30)
    for result in results:
        result["is_added"] = False
    return jsonify(results)


@bp.route('/search', methods=["GET"])
@jwt_required()
def search():
    """
    Search for a word in the dictionary. The search can be based on:
    - simplified
    - pinyin
    - definitions
    Expects: /search?type=xxx
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

        return jsonify(results)

    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
