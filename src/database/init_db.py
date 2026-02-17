from sqlalchemy.sql import text

def create_tables(conn):
    with open('sql/create_tables.sql', 'r') as create_tables:
        sql_script = create_tables.read()
    queries = sql_script.split(';') # Split the script into individual queries by splitting on ;
    queries.pop() # Delete last 'query' since it is always empty due to the last ; 

    try:
        for query in queries:
            conn.execute(text(query))
    except Exception as e:
        print("Error during create_tables:", e)

def drop_tables(conn):
    with open('sql/drop_tables.sql', 'r') as drop_tables:
        sql_script = drop_tables.read()
    queries = sql_script.split(';')
    queries.pop()

    try:
        for query in queries:
            conn.execute(text(query))
    except Exception as e:
        print("Error during drop_tables:", e)