# # Only responsible for reading from the raw data in the data/ directory 
# # this file will read .csv files and put the data into a pandas dataframe

# import pandas as pd

# def read_csv(filepath):
#     try:
#         df = pd.read_csv(filepath)
#         return df
#     except FileNotFoundError:
#         raise FileNotFoundError("Wrong filepath or file does not exist")
    
#     except Exception as e:
#         raise RuntimeError("something unintended happened when reading csv") from e
#     # we exception as e to not lose the error if error happens on line 12 upto 13, it will output none. 

import pandas as pd

def read_source(source_config):
    source_type = source_config["type"]
    paths = source_config["path"]

    dataframes = []

    for path in paths:
        if source_type == "csv":
            df = pd.read_csv(
                path,
                delimiter=source_config.get("delimiter", ","),
                header=0 if source_config.get("has_header", True) else None
            )

        elif source_type == "json":
            df = pd.read_json(path)

        else:
            raise ValueError(f"Unsupported source type: {source_type}")

        dataframes.append(df)

    return pd.concat(dataframes, ignore_index=True)