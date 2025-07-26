import psycopg2
from psycopg2 import pool
import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()
DB_POOL = pool.ThreadedConnectionPool(
    minconn=5,
    maxconn=10,
    dbname=os.getenv("DB_NAME"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASS"),
    host=os.getenv("DB_HOST"),
    port=os.getenv("DB_PORT")
)

def get_conn():
    return DB_POOL.getconn()

def put_conn(conn):
    DB_POOL.putconn(conn)

    