import re
from app.db import get_db
from app.models.sentences import get_sentences_by_ids
from pypinyin import pinyin, Style

# Optional: find a better pinyin converter and use pinyin from sql

def get_search_results(field: str, query: str, limit: int = 30):
    """
    Retrieve search results from the dictionary based on the specified field and query.
    Field must be one of 'simplified', 'pinyin_normalized', 'definitions', or 'id'.
    Returns a list of dictionaries with 'id', 'simplified', 'pinyin', 'definitions', and 'sentences'.
    """
    if field == "id":
        return [get_word_by_id(int(query))]
    else:
        sql = f"""
            SELECT id, simplified, definitions, sentence_ids
            FROM dictionary
            WHERE {field} %% %s
            ORDER BY SIMILARITY({field}, %s) DESC
            LIMIT %s;
            """
        params = (query, query, limit)
    
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute(sql, params)
    rows = cursor.fetchall()

    all_sentence_ids = [sentence_id for row in rows for sentence_id in row[3]]
    sentences = get_sentences_by_ids(all_sentence_ids)

    results = []
    for row in rows:
        id, simplified, definitions, sentence_ids = row
        pinyin_ = ''.join(syllable[0] for syllable in pinyin(simplified, style=Style.TONE))
        word = {"id": id,
                "simplified": simplified,
                "pinyin": pinyin_,
                "definitions": definitions.split("/")[1:-1],
                "sentences": [sentences[sid] for sid in sentence_ids]}
        results.append(word)

    cursor.close()
    conn.close()
    return results


def get_word_by_id(id: int):
    """
    Retrieve a word's detail from the dictionary.
    Returns a dictionary with 'id', 'simplified', 'pinyin', 'definitions', and 'sentences'.
    """
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("SELECT simplified, definitions, sentence_ids FROM dictionary WHERE id = %s", (id,))
    row = cursor.fetchone()

    if row:
        simplified = row[0]
        pinyin_ = ''.join(syllable[0] for syllable in pinyin(simplified, style=Style.TONE))
        definitions = row[1].split("/")[1:-1]
        sentences = get_sentences_by_ids(row[2]) if row[2] else []
        result = {"id": id, 
                  "simplified": simplified,
                  "pinyin": pinyin_,
                  "definitions": definitions,
                  "sentences": [sentences[sid] for sid in row[2]]}
        cursor.close()
        conn.close()
        return result

    cursor.close()
    conn.close()
    return None


if __name__ == "__main__":
    conn = get_db()
    cursor = conn.cursor()
    batch_size = 1000
    batch = []

    with open("/Users/anthonylin/Downloads/cedict_ts.u8", encoding="utf-8") as f:
        for line in f:
            if line.startswith("#"):
                continue

            match = re.match(r"(\S+)\s+(\S+)\s+\[(.+?)\]\s+/(.+)/", line)
            if not match:
                continue

            trad, simp, pinyin, defs = match.groups()
            definitions = "/" + defs.strip("/") + "/"
            batch.append((simp, pinyin, definitions))
            if len(batch) >= batch_size:
                cursor.executemany(
                    "INSERT INTO dictionary (simplified, pinyin, definitions) VALUES (%s, %s, %s)",
                    batch
                )
                print(f"Inserted {len(batch)} records into the database.")
                batch.clear()
                conn.commit()
                
        
        if batch:
            cursor.executemany(
                "INSERT INTO dictionary (simplified, pinyin, definitions) VALUES (%s, %s, %s)",
                batch
            )
            conn.commit()
            batch.clear()
            


    cursor.close()
    conn.close()
    print("Dictionary loaded successfully.")