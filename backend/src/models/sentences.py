from src.db import get_conn, put_conn

def get_sentences_by_ids(sentence_ids: list[int]) -> dict:
    """
    Retrieve sentences by their IDs. Returns a dictionary of sentences (key=sentence_id), 
    where each sentence is represented as a dictionary with 'sentence_id', 'chinese', 
    'pinyin', and 'english'.
    """
    if not sentence_ids:
        return {}

    conn = get_conn()  
    with conn.cursor() as cursor:
        cursor.execute(
            "SELECT sentence_id, chinese, english, pinyin FROM sentences WHERE sentence_id = ANY(%s)",
            (sentence_ids,)
        )
        results = cursor.fetchall()
        sentences = {}
        for row in results:
            sentences[row[0]] =  {'sentence_id': row[0],
                                'chinese': row[1], 
                                'pinyin': row[3],
                                'english': row[2]}

    put_conn(conn)
    return sentences