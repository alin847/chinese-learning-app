from src.db import get_db


def create_user(name: str, email: str, password_hash: str) -> str:
    """
    Creates a new user in the database. Returns the user ID on success.
    """
    conn = get_db()

    try:
        with conn.cursor() as cursor:
            cursor.execute(
                "INSERT INTO users (name, email, password_hash) VALUES (%s, %s, %s) RETURNING user_id",
                (name, email, password_hash)
            )
            user_id = cursor.fetchone()[0]
            conn.commit()
            return user_id
    except Exception as e:
        conn.rollback()
        raise Exception(f"Error creating user: {e}")
    finally:
        conn.close()


def get_user_by_id(user_id: str) -> dict:
    """
    Retrieve a user by ID. Returns user data as a dictionary or None if not found.
    
    {
        "user_id": "user_id",
        "name": "user_name",
        "email": "user_email"
        "password_hash": "hashed_password"
    }
    """
    conn = get_db()

    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT name, email, password_hash FROM users WHERE user_id = %s", (user_id,))
            user = cursor.fetchone()
            if user:
                return {
                    "user_id": user_id,
                    "name": user[0],
                    "email": user[1],
                    "password_hash": user[2]
                }
            return None
    except Exception as e:
        raise Exception(f"Error retrieving user: {e}")
    finally:
        conn.close()
    

def get_user_by_email(email: str) -> dict:
    """
    Retrieve a user by email. Returns user data as a dictionary or None if not found.

    {
        "user_id": "user_id",
        "name": "user_name",
        "email": "user_email",
        "password_hash": "hashed_password"
    }
    """
    conn = get_db()

    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT user_id, name, password_hash FROM users WHERE email = %s", (email,))
            user = cursor.fetchone()
            if user:
                return {
                    "user_id": user[0],
                    "name": user[1],
                    "email": email,
                    "password_hash": user[2]
                }
            return None
    except Exception as e:
        raise Exception(f"Error retrieving user by email: {e}")
    finally:
        conn.close()


def delete_user(user_id: str) -> bool:
    """
    Deletes all of a user's data by ID. Returns True on success.
    """
    conn = get_db()

    try:
        with conn.cursor() as cursor:
            # Delete user from the database
            cursor.execute("DELETE FROM users WHERE user_id = %s", (user_id,))
            # Delete associated vocab_bank entries
            cursor.execute("DELETE FROM vocab_bank WHERE user_id = %s", (user_id,))
            conn.commit()
            return True
    except Exception as e:
        conn.rollback()
        raise Exception(f"Error deleting user: {e}")
    finally:
        conn.close()
