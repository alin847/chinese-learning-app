from ..db import get_db
from ..models.sentences import get_sentences_by_ids
from pypinyin import pinyin, Style
from typing import Union

# Optional: find a better pinyin converter and use pinyin from sql
def get_search_results(field: str, query: str, limit: int = 30) -> list[dict]:
    """
    Retrieve search results from the dictionary based on the specified field and query.
    Field must be one of 'simplified', 'pinyin_normalized', 'definitions', or 'simplified_id'.

    Returns a list of dictionaries with 'simplified_id', 'simplified', 'pinyin', 'definitions', and 'sentences'.
    Returns an empty list if no results are found.
    """
    if field not in ['simplified', 'pinyin_normalized', 'definitions', 'simplified_id']:
        raise ValueError("Field must be one of 'simplified', 'pinyin_normalized', 'definitions', or 'simplified_id'.")
    
    if field == "simplified_id":
        word = get_word_by_id(int(query))
        if not word:
            return []
        return [word]

    sql = f"""
        SELECT simplified_id, simplified, definitions, sentence_ids
        FROM dictionary
        WHERE {field} %% %s
        ORDER BY SIMILARITY({field}, %s) DESC
        LIMIT %s;
        """
    params = (query, query, limit)
    
    conn = get_db()
    cursor = conn.cursor()
    try:
        cursor.execute(sql, params)
        rows = cursor.fetchall()

        all_sentence_ids = list({sentence_id for row in rows for sentence_id in row[3]})
        sentences = get_sentences_by_ids(all_sentence_ids)

        results = []
        for row in rows:
            simplified_id, simplified, definitions, sentence_ids = row
            pinyin_ = ''.join(syllable[0] for syllable in pinyin(simplified, style=Style.TONE))
            word = {"simplified_id": simplified_id,
                    "simplified": simplified,
                    "pinyin": pinyin_,
                    "definitions": definitions.split("/")[1:-1],
                    "sentences": [sentences[sid] for sid in sentence_ids]}
            results.append(word)
        return results
    except Exception as e:
        raise Exception(f"Error retrieving search results: {e}")
    finally:
        cursor.close()
        conn.close()


def get_word_by_id(simplified_id: Union[int, list]) -> Union[dict, list[dict]]:
    """
    Retrieve a word's detail from the dictionary by its simplified_id(s).

    Returns a dictionary with 'simplified_id', 'simplified', 'pinyin', 'definitions', and 'sentences'.
    If simplified_id is a list of integers, it returns a list of dictionaries for each simplified_id.
    """
    conn = get_db()
    cursor = conn.cursor()
    if isinstance(simplified_id, int):
        cursor.execute("SELECT simplified, definitions, sentence_ids FROM dictionary WHERE simplified_id = %s", (simplified_id,))
        row = cursor.fetchone()

        if row:
            simplified = row[0]
            pinyin_ = ''.join(syllable[0] for syllable in pinyin(simplified, style=Style.TONE))
            definitions = row[1].split("/")[1:-1]
            sentences = get_sentences_by_ids(row[2]) if row[2] else []
            result = {
                    "simplified_id": simplified_id, 
                    "simplified": simplified,
                    "pinyin": pinyin_,
                    "definitions": definitions,
                    "sentences": [sentences[sid] for sid in row[2]]}
            cursor.close()
            conn.close()
            return result
    elif isinstance(simplified_id, list):
        cursor.execute("SELECT simplified_id, simplified, definitions, sentence_ids FROM dictionary WHERE simplified_id = ANY(%s)", (simplified_id,))
        rows = cursor.fetchall()
        sentence_ids = list({sid for row in rows for sid in row[3]})
        sentences = get_sentences_by_ids(sentence_ids)

        results = []
        # Ensure results are in the same order as simplified_id input
        row_map = {row[0]: row for row in rows}
        for id_ in simplified_id:
            row = row_map[id_]
            _, simplified, definitions, sentence_ids = row
            pinyin_ = ''.join(syllable[0] for syllable in pinyin(simplified, style=Style.TONE))
            result = {
                "simplified_id": id_,
                "simplified": simplified,
                "pinyin": pinyin_,
                "definitions": definitions.split("/")[1:-1],
                "sentences": [sentences[sid] for sid in sentence_ids]}
            results.append(result)
        cursor.close()
        conn.close()
        return results

    cursor.close()
    conn.close()
    return None

def get_word_ids_by_hsk(level: int) -> list[int]:
    """
    Retrieve all word IDs for a given HSK level.
    
    Returns a list of simplified_ids for the specified HSK level.
    """
    conn = get_db()
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT simplified_id FROM dictionary WHERE level = %s", (str(level),))
            rows = cursor.fetchall()
            ids = [row[0] for row in rows]
            return ids
    except Exception as e:
        raise Exception(f"Error retrieving word IDs for HSK level {level}: {e}")
    finally:
        conn.close()


if __name__ == "__main__":
    pass
