from src.db import get_conn, put_conn
from src.models.dictionary import get_word_by_id
from psycopg2.extras import execute_values

def add_vocab(user_id: str, simplified_id: int) -> bool:
    """
    Adds a new vocabulary word (simplified_id) in the database for user_id. Returns True on success.
    """
    conn = get_conn()

    try:
        with conn.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO vocab_bank (user_id, simplified_id) 
                VALUES (%s, %s);""",
                (user_id, simplified_id)
            )

            cursor.execute("""
                        UPDATE dictionary
                        SET frequency = frequency + 1
                        WHERE simplified_id = %s;""", (simplified_id,))
            conn.commit()
            return True
    except Exception as e:
        conn.rollback()
        raise Exception(f"Error adding vocabulary word: {e}")
    finally:
        put_conn(conn)


def add_vocab_batch(user_id: str, simplified_ids: list, repetitions: list, intervals: list, next_review: list) -> bool:
    """
    Adds a batch of vocabulary words to the database for user_id. Returns true on success.
    """
    conn = get_conn()
    
    if not (len(simplified_ids) == len(repetitions) == len(intervals) == len(next_review)):
        raise ValueError("All input lists must have the same length.")
    
    try:
        with conn.cursor() as cursor:
            rows = [(user_id, simplified_ids[i], repetitions[i], intervals[i], next_review[i]) 
                    for i in range(len(simplified_ids))]
            execute_values(
                cursor, 
                """
                INSERT INTO vocab_bank (user_id, simplified_id, repetitions, interval, next_review) 
                VALUES %s 
                """, 
                rows)

            cursor.execute(
                """
                UPDATE dictionary
                SET frequency = frequency + 1
                WHERE simplified_id = ANY(%s)
                """,
                (simplified_ids, )
            )
            conn.commit()
            return True
    except Exception as e:
        conn.rollback()
        raise Exception(f"Error adding batch vocabulary words: {e}")
    finally:
        put_conn(conn)


def update_vocab(user_id: str, vocab: dict) -> bool:
    """
    Update an existing vocabulary word in the database. Vocab should be a dictionary with the
    necessary fields: 

        {
            'simplified_id': int,
            'repetitions': int,
            'interval': int,
            'ease_factor': float,
        }
    Returns True on success.
    """
    conn = get_conn()

    try:
        with conn.cursor() as cursor:
            cursor.execute(
                """
                UPDATE vocab_bank
                SET repetitions = %s, interval = %s, ease_factor = %s,
                    last_reviewed = CURRENT_DATE, next_review = CURRENT_DATE + (%s)::int,
                    updated_at = NOW()
                WHERE user_id = %s AND simplified_id = %s
                """,
                (vocab["repetitions"], vocab["interval"], vocab["ease_factor"],
                 vocab["interval"], user_id, vocab["simplified_id"])
            )
            conn.commit()
            return True
    except Exception as e:
        conn.rollback()
        raise Exception(f"Error updating vocabulary word: {e}")
    finally:
        put_conn(conn)
    

def get_vocab(user_id: str, simplified_id: int) -> dict:
    """
    Retrieve a vocabulary word by user_id and simplified_id. Returns a dictionary with the following
    fields: 
    
        {
            "vocab_bank_id": int,  # ID of the vocabulary bank entry
            "simplified_id": int,  # ID of the simplified character
            "repetitions": int,  # Number of repetitions
            "interval": int,  # Interval for the next review
            "ease_factor": float,  # Ease factor for the vocabulary word
            "last_reviewed": date,  # Date of the last review
            "next_review": date,  # Date of the next review
        }
    Returns None if the vocabulary word is not found.
    """
    conn = get_conn()

    try:
        with conn.cursor() as cursor:
            cursor.execute("""
                           SELECT vocab_bank_id, simplified_id, repetitions, interval, ease_factor, last_reviewed, next_review FROM vocab_bank 
                           WHERE user_id = %s AND simplified_id = %s""", 
                           (user_id, simplified_id))
            row = cursor.fetchone()
            if row:
                return {"vocab_bank_id": row[0],
                        "simplified_id": row[1],
                        "repetitions": row[2],
                        "interval": row[3],
                        "ease_factor": row[4],
                        "last_reviewed": row[5],
                        "next_review": row[6]}
            return None
    except Exception as e:
        raise Exception(f"Error retrieving vocabulary word: {e}")
    finally:
        put_conn(conn)
    

def get_all_vocab(user_id: str) -> list:
    """
    Retrieve all vocabulary words for a user. Returns a list of dictionaries sorted by next_review
    in ascending order.
    
    Dictionaries contain the following fields:
    - 'vocab_bank_id': int,  # ID of the vocabulary bank entry
    - 'simplified_id': int,  # ID of the simplified character
    - 'repetitions': int,  # Number of repetitions
    - 'interval': int,  # Interval for the next review
    - 'ease_factor': float,  # Ease factor for the vocabulary word
    - 'last_reviewed': date,  # Date of the last review
    - 'next_review': date,  # Date of the next review
    
    Returns an empty list if no vocabulary words are found.
    """
    conn = get_conn()

    try:
        with conn.cursor() as cursor:
            cursor.execute("""
                           SELECT vocab_bank_id, simplified_id, repetitions, interval, ease_factor, last_reviewed, next_review 
                           FROM vocab_bank WHERE user_id = %s 
                           ORDER BY next_review ASC
                           """, 
                           (user_id,))
            rows = cursor.fetchall()
            return [{"vocab_bank_id": row[0],
                    "simplified_id": row[1],
                    "repetitions": row[2],
                    "interval": row[3],
                    "ease_factor": row[4],
                    "last_reviewed": row[5],
                    "next_review": row[6]} for row in rows]
    except Exception as e:
        raise Exception(f"Error retrieving all vocabulary words: {e}")
    finally:
        put_conn(conn)


def delete_vocab(user_id: str, simplified_id: int) -> bool:
    """
    Delete a vocabulary word by user ID and simplified id. Returns True on success.
    """
    conn = get_conn()

    try:
        with conn.cursor() as cursor:
            cursor.execute("""
                           DELETE FROM vocab_bank 
                           WHERE user_id = %s AND simplified_id = %s
                           """, 
                           (user_id, simplified_id))
            cursor.execute("""
                           UPDATE dictionary
                           SET frequency = frequency - 1
                           WHERE simplified_id = %s;""", (simplified_id,))
            
            conn.commit()
            return True
    except Exception as e:
        conn.rollback()
        raise Exception(f"Error deleting vocabulary word: {e}")
    finally:
        put_conn(conn)


def get_random_vocab(user_id: str, limit: int = 20) -> list[dict]:
    """
    Retrieve random new vocabulary words for a user to learn by using weighted frequencies.
    
    Returns a list of dictionary with the following fields:
    - 'simplified_id': int,  # ID of the vocabulary word
    - 'simplified': str,  # Simplified character
    - 'pinyin': str,  # Pinyin representation
    - 'definitions': list,  # List of definitions
    - 'sentence_ids': list,  # List of example sentences
    """
    conn = get_conn()
    
    all_vocab = get_all_vocab(user_id)
    excluded_simplified_ids = (vocab['simplified_id'] for vocab in all_vocab) if all_vocab else (-1,)

    try:
        with conn.cursor() as cursor:
            cursor.execute("""
                        SELECT simplified_id, frequency
                        FROM dictionary
                        WHERE simplified_id NOT IN %s
                        ORDER BY -LOG(random()) / frequency
                        LIMIT %s;""", (tuple(excluded_simplified_ids), limit))
            rows = cursor.fetchall()
            simplified_ids = [row[0] for row in rows]
            return get_word_by_id(simplified_ids)
    except Exception as e:
        raise Exception(f"Error retrieving random vocabulary words: {e}")
    finally:
        put_conn(conn)

def get_random_practice(user_id: str, limit: int = 10) -> list[dict]:
    """
    Retrieve random vocabulary words for practice that are due for review. If there are less 
    words due than limit, then it will add the most recent words that are not due for review 
    yet to fill the limit.
    
    Returns a list of dictionaries with the following fields:
    - 'simplified_id': int,  # ID of the vocabulary word
    - 'simplified': str,  # Simplified character
    - 'definitions': list,  # List of definitions
    """ 
    try:
        all_vocab = get_all_vocab(user_id)
        due_vocab = all_vocab[:limit]
        simplified_ids = [vocab['simplified_id'] for vocab in due_vocab]
        
        conn = get_conn()
        results = []
        with conn.cursor() as cursor:
            cursor.execute("""
                           SELECT simplified_id, simplified, definitions 
                           FROM dictionary 
                           WHERE simplified_id = ANY(%s)""", (simplified_ids,))
            rows = cursor.fetchall()
        put_conn(conn)
        for row in rows:
            simplified_id, simplified, definitions = row
            vocab = {
                'simplified_id': simplified_id,
                'simplified': simplified,
                'definitions': definitions.split("/")[1:-1]
            }
            results.append(vocab)
        return results
    except Exception as e:
        raise Exception(f"Error retrieving random practice vocabulary words: {e}")

