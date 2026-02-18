from src.database.connection import get_connection
import sqlalchemy

def test_get_connection():
    with get_connection() as conn:
        assert isinstance(conn, sqlalchemy.Connection)