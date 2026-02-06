# Only responsible for reading from the raw data in the data/ directory 
# this file will read .csv files and put the data into a pandas dataframe

import pandas as pd

def read_csv(filepath):
    try:
        df = pd.read_csv(filepath)
        return df
    except FileNotFoundError:
        raise FileNotFoundError("Wrong filepath or file does not exist")
    # except Exception:
    #     print("Something unintended happened when reading csv")
    
    except Exception as e:
        raise RuntimeError("something unintended happened when reading csv") from e
    # we exception as e to not lose the error if error happens on line 12 upto 13, it will output none. 