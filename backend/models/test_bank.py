from backend.db import get_db

def get_random_question(level: int, excluded: list) -> dict:
    """
    Fetch a random question from the test bank based on the specified level.
    Excludes questions that are already in the excluded list. 
    
    Returns a dictionary with the question details or an empty dictionary if no question is found.
    The dictionary contains:
    - 'question_id': The ID of the question
    - 'text': The text of the question
    - 'answer': The correct answer to the question
    - 'options': A list of options for the question
    """
    conn = get_db()

    try:
        with conn.cursor() as cursor:
            excluded = tuple(excluded) if excluded else (-1,)
            cursor.execute(
                """
                SELECT question_id, text, answer, options
                FROM test_bank
                WHERE level = %s AND question_id NOT IN %s
                ORDER BY RANDOM()
                LIMIT 1;
                """,
                (str(level), tuple(excluded))
            )
            row = cursor.fetchone()
            if row:
                return {
                    'question_id': row[0],
                    'text': row[1],
                    'answer': row[2],
                    'options': row[3]
                }
            else:
                return {}
    except Exception as e:
        raise Exception(f"Error retrieving random question: {e}")
    finally:
        conn.close()