from flask import Blueprint, render_template, request, redirect, url_for, jsonify
from flask_login import login_required, current_user
from app.models.dictionary import get_search_results
from app.models.vocab_bank import get_vocab, get_all_vocab, add_vocab, update_vocab

bp = Blueprint('search', __name__)    
# Perhaps caching???
@bp.route('/search/<search_type>/<query>')
@login_required
def search_query(search_type, query):
    """Search for a query in the dictionary and render results."""
    KEY = {"simplified": "simplified",
           "pinyin": "pinyin_normalized",
           "definitions": "definitions",
           "id": "id"}
    results = get_search_results(KEY[search_type], query)
    all_vocab = get_all_vocab(current_user.id)
    # Convert all_vocab to a set for faster lookup
    all_vocab_set = {vocab["simplified_id"] for vocab in all_vocab}

    for result in results:
        # Fetch is_added status
        result["is_added"] = True if result["id"] in all_vocab_set else False

    return render_template('search.html', user=current_user, results=results)


@bp.route('/search', methods=["GET"])
@login_required
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
    
