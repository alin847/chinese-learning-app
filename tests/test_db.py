from backend.db import get_db

def test_db_connection():
    conn = get_db()
    assert conn is not None
