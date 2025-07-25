from src.db import get_db


def get_progress(user_id: str) -> dict:
    """
    Retrieve the progress of a user. Returns a dictionary with counts of words in different states.

    The dictionary contains:
    - 'learning_vocab': Count of words in the learning state (0-1 repetitions)
    - 'reviewing_vocab': Count of words in the reviewing state (2-3 repetitions
    - 'mastered_vocab': Count of words in the mastered state (4+ repetitions)
    - 'time_spent': Total time spent by the user
    - 'practice_completed': Total number of practices completed by the user
    """
    conn = get_db()

    try:
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT 
                    SUM(CASE WHEN repetitions BETWEEN 0 AND 1 THEN 1 ELSE 0 END) AS learning_count,
                    SUM(CASE WHEN repetitions BETWEEN 2 AND 3 THEN 1 ELSE 0 END) AS reviewing_count,
                    SUM(CASE WHEN repetitions >= 4 THEN 1 ELSE 0 END) AS mastered_count
                FROM vocab_bank
                WHERE user_id = %s
            """, (user_id,))

            result = cursor.fetchone()
            progress = {
                'learning_count': result[0],
                'reviewing_count': result[1],
                'mastered_count': result[2]
            }
            cursor.execute("""
                SELECT time_spent, practice_completed FROM users WHERE user_id = %s
            """, (user_id,))
            user_data = cursor.fetchone()
            progress['time_spent'] = user_data[0]
            progress['practice_completed'] = user_data[1]
            return progress
    except Exception as e:
        raise Exception(f"Error retrieving user progress: {e}")
    finally:
        conn.close()

    return progress

def add_time_spent(user_id: str, time_spent: int):
    """
    Add time spent by the user to their progress. Return True if success.
    """
    conn = get_db()
    try:
        with conn.cursor() as cursor:
            cursor.execute("""
                UPDATE users
                SET time_spent = time_spent + %s
                WHERE user_id = %s
            """, (time_spent, user_id))

            conn.commit()
            return True
    except Exception as e:
        conn.rollback()
        raise Exception(f"Error updating time spent: {e}")
    finally:
        conn.close()
        

def add_practice_completed(user_id: str):
    """
    Increment the practice completed count for the user.
    """
    conn = get_db()
    try:
        with conn.cursor() as cursor:
            cursor.execute("""
                UPDATE users
                SET practice_completed = practice_completed + 1
                WHERE user_id = %s
            """, (user_id,))

            conn.commit()
            return True
    except Exception as e:
        conn.rollback()
        raise Exception(f"Error updating practice completed: {e}")
    finally:
        conn.close()
 