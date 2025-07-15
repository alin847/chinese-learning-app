from app.db import get_db
from pypinyin import pinyin, Style


def get_sentences_by_character(character: str, limit: int = 3):
    """
    Retrieve sentences containing the specified character from the database.
    Returns a list of sentences, each represented as a dictionary with 'id', 'chinese',
    'pinyin' and 'english'.
    """
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT id, chinese, english FROM sentences WHERE chinese ILIKE %s LIMIT %s",
        (f"%{character}%", limit)
    )
    
    results = cursor.fetchall()
    sentences = [{'id': row[0],
                  'chinese': row[1], 
                  'pinyin': ''.join(val[0] for val in pinyin(row[1], style=Style.TONE)),
                  'english': row[2]} for row in results]

    cursor.close()
    conn.close()

    return sentences


def get_sentences_by_ids(sentence_ids: list[int]):
    """
    Retrieve sentences by their IDs. Returns a dictionary of sentences (key=id), where each sentence
    is represented as a dictionary with 'id', 'chinese', 'pinyin', and 'english'.
    """
    if not sentence_ids:
        return {}

    conn = get_db()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT id, chinese, english, pinyin FROM sentences WHERE id = ANY(%s)",
        (sentence_ids,)
    )
    
    results = cursor.fetchall()
    sentences = {}
    for row in results:
        sentences[row[0]] =  {'id': row[0],
                              'chinese': row[1], 
                              'pinyin': row[3],
                              'english': row[2]}

    cursor.close()
    conn.close()

    return sentences