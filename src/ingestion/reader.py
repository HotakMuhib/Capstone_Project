# import pandas as pd

# def read_source(source_config):
#     source_type = source_config["type"]
#     paths = source_config["paths"]

#     dfs = []

#     for path in paths:
#         if source_type == "csv":
#             df = pd.read_csv(
#                 path,
#                 delimiter=source_config.get("delimiter", ","),
#                 header=0 if source_config.get("has_header", True) else None
#             )
#         elif source_type == "json":
#             df = pd.read_json(path)
#         else:
#             raise ValueError(f"Unsupported source type: {source_type}")

#         dfs.append(df)

#     return pd.concat(dfs, ignore_index=True)