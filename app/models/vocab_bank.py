from app.db import get_db


def add_vocab(user_id: str, simplified_id: int) -> int:
    """
    Adds a new vocabulary word in the database, where the vocabulary word is from dictionary
    database. Returns the ID on success, None on failure.
    """
    conn = get_db()
    if conn is None:
        return None

    try:
        # Fetch the simplified character from the dictionary
        with conn.cursor() as cursor:
            cursor.execute(
                "SELECT simplified FROM dictionary WHERE id = %s", (simplified_id,)
            )
            row = cursor.fetchone()
            if not row:
                print("Character not found in dictionary.")
                return None
            simplified = row[0]

        with conn.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO vocab_bank (user_id, simplified_id, simplified) 
                VALUES (%s, %s, %s) 
                RETURNING id;""",
                (user_id, simplified_id, simplified)
            )
            id = cursor.fetchone()[0]
            conn.commit()
            return id
    except Exception as e:
        print("Error adding vocabulary word:", e)
        conn.rollback()
        return None
    finally:
        conn.close()


def update_vocab(user_id: str, vocab: dict) -> bool:
    """
    Update an existing vocabulary word in the database. Vocab should be a dictionary with the
    necessary fields: simplified_id, repetitions, interval, ease_factor.
    """

    conn = get_db()
    if conn is None:
        return False

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
        print("Error updating vocabulary word:", e)
        conn.rollback()
        return False
    finally:
        conn.close()
    

def get_vocab(user_id, simplified_id):
    """
    Retrieve a vocabulary word by user ID and simplified id. Returns a dictionary with the following
    fields: id, simplified_id, simplified, repetitions, interval, ease_factor, last_reviewed, next_review,
    or None if not found or an error occurs.
    """
    conn = get_db()
    if conn is None:
        return None

    try:
        with conn.cursor() as cursor:
            cursor.execute("""
                           SELECT * FROM vocab_bank 
                           WHERE user_id = %s AND simplified_id = %s""", 
                           (user_id, simplified_id))
            row = cursor.fetchone()
            if row:
                return {"id": row[0],
                        "simplified_id": row[2],
                        "simplified": row[3],
                        "repetitions": row[4],
                        "interval": row[5],
                        "ease_factor": row[6],
                        "last_reviewed": row[7],
                        "next_review": row[8]}
            return None
    except Exception as e:
        print("Error retrieving character:", e)
        return None
    finally:
        conn.close()
    

def get_all_vocab(user_id):
    """
    Retrieve all vocabulary words for a user. Returns a list of dictionaries sorted by new_review
    in ascending order.
    Dictionaries contain the following fields:
    id, simplified_id, simplified, repetitions, interval, ease_factor, last_reviewed, next_review.
    """
    conn = get_db()
    if conn is None:
        return []

    try:
        with conn.cursor() as cursor:
            cursor.execute("""
                           SELECT * FROM vocab_bank WHERE user_id = %s 
                           ORDER BY next_review ASC
                           """, 
                           (user_id,))
            rows = cursor.fetchall()
            return [{"id": row[0],
                    "simplified_id": row[2],
                    "simplified": row[3],
                    "repetitions": row[4],
                    "interval": row[5],
                    "ease_factor": row[6],
                    "last_reviewed": row[7],
                    "next_review": row[8]} for row in rows]
        
    except Exception as e:
        print("Error retrieving characters:", e)
        return []
    finally:
        conn.close()


def delete_vocab(user_id, simplified_id):
    """
    Delete a vocabulary word by user ID and simplified id. Returns True on success, False on failure.
    """
    conn = get_db()
    if conn is None:
        return False

    try:
        with conn.cursor() as cursor:
            cursor.execute("""
                           DELETE FROM vocab_bank 
                           WHERE user_id = %s AND simplified_id = %s
                           """, 
                           (user_id, simplified_id))
            conn.commit()
            return True
    except Exception as e:
        print("Error deleting vocabulary word:", e)
        conn.rollback()
        return False
    finally:
        conn.close()


def SM2(score, repetitions, interval, ease_factor):
    """SM-2 algorithm for spaced repetition."""
    if score >= 3:  # Correct answer
        if repetitions == 0:
            interval = 1
        elif repetitions == 1:
            interval = 6
        else:
            interval = round(interval * ease_factor)
        repetitions += 1
    else:  # Incorrect answer
        repetitions = 0
        interval = 1
        
    ease_factor = max(1.3, ease_factor + (0.1 - (5 - score) * (0.08 + (5 - score) * 0.02)))
    
    return (repetitions, interval, ease_factor)
