from src.database.connection import get_connection
from src.database.init_db import drop_tables

with get_connection() as conn:
    drop_tables(conn)
    conn.commit()