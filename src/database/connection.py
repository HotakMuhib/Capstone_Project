# # Create and close postgresql connection to our AWS database
# # will allow loader.py to interact with the database

import os
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from dotenv import load_dotenv

def get_connection():
    load_dotenv(override=True)
    conn = None
    try:
        host = os.getenv("HOST"),
        port = os.getenv("PORT"),
        database = os.getenv("DB_NAME"),
        user = os.getenv("USER"),
        password = os.getenv("PASSWORD"),
        #sslmode = os.getenv("SSLMODE"),
        #sslrootcert = os.getenv("SSLROOTCERT")

        db_url_str = f'postgresql+psycopg2://{user[0]}:{password[0]}@{host[0]}:{port[0]}/{database[0]}'
        engine = create_engine(db_url_str)
        conn = engine.connect()

    except Exception as e:
        print(f"Database error: {e}")
        raise

    return conn
    