from app.db import get_db
from flask_login import UserMixin

class User(UserMixin):
    """User model for Flask-Login integration."""
    def __init__(self, id, email, password_hash):
        self.id = id
        self.email = email
        self.password_hash = password_hash

    def get_id(self):
        return str(self.id)


def create_user(email, password_hash):
    """Create a new user in the database. Returns the user ID on success, None on failure."""
    conn = get_db()
    if conn is None:
        return None

    try:
        with conn.cursor() as cursor:
            cursor.execute(
                "INSERT INTO users (email, password_hash) VALUES (%s, %s) RETURNING id",
                (email, password_hash)
            )
            user_id = cursor.fetchone()[0]
            conn.commit()
            return user_id
    except Exception as e:
        print("Error creating user:", e)
        conn.rollback()
        return None
    finally:
        conn.close()  # Ensure the connection is closed after use


def get_user_by_id(user_id):
    """Retrieve a user by ID. Returns user data as an User Object."""
    conn = get_db()
    if conn is None:
        return None

    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
            user = cursor.fetchone()
            if user:
                return User(id=user[0], email=user[1], password_hash=user[2])
            return None
    except Exception as e:
        print("Error retrieving user:", e)
        return None
    finally:
        conn.close()  # Ensure the connection is closed after use
    

def get_user_by_email(email):
    """Retrieve a user by email. Returns user data as an User Object."""
    conn = get_db()
    if conn is None:
        return None

    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
            user = cursor.fetchone()
            if user:
                return User(id=user[0], email=user[1], password_hash=user[2])
            return None
    except Exception as e:
        print("Error retrieving user:", e)
        return None
    finally:
        conn.close()  # Ensure the connection is closed after use


def delete_user(user_id):
    """Delete a user by ID. Returns True on success, False on failure."""
    conn = get_db()
    if conn is None:
        return False

    try:
        with conn.cursor() as cursor:
            cursor.execute("DELETE FROM users WHERE id = %s", (user_id,))
            conn.commit()
            return True
    except Exception as e:
        print("Error deleting user:", e)
        conn.rollback()
        return False
    finally:
        conn.close()  # Ensure the connection is closed after use