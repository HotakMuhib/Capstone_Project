# optional second reader file if we want to add .json file reading capabilities

# Only responsible for reading from the raw data in the data/ directory 
# this file will read .json files and put the data into a pandas dataframe

import pandas as pd

def read_json(filepath):
    try:
        df = pd.read_json(filepath)
        return df
    except FileNotFoundError:
        raise FileNotFoundError("wrong filepath or file does not exist")
    
    except Exception as e:
        raise RuntimeError("something uninteded happened when reading json") from e

    # we exception as e to not lose the error if error happens on line 12 upto 13, it will output none. 
