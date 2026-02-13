# # Create and close postgresql connection to our AWS database
# # will allow loader.py to interact with the database
# from sqlalchemy import create_engine

# def get_engine(db_config):
#     user = db_config["user"]
#     password = db_config["password"]
#     host = db_config["host"]
#     port = db_config["port"]
#     name = db_config["name"]

#     connection_string = f"postgresql://{user}:{password}@{host}:{port}/{name}"

#     engine = create_engine(connection_string)
#     return engine