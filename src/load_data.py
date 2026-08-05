import pandas as pd
from src.logger_config import logging
import os

def load_raw_data(filepath:str) -> pd.DataFrame:

    if not os.path.exists(filepath):
        logging.error("file path does not exist")
        raise FileNotFoundError(f"the file is not found {filepath}")
    
    try:
        df=pd.read_parquet(filepath,engine="pyarrow")
        logging.info("file is accesed")
    except Exception as e:
        raise RuntimeError(f"error occured {e}")
    
    return df 

