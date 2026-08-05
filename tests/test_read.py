import pandas as pd
from src.load_data import load_raw_data

df=load_raw_data(r"C:\Users\Shubham Chouhan\OneDrive\Desktop\analysis\data\raw\yellow_tripdata_2026-01.parquet")#to work with parquet files you must install pyarrow
print(df.head(3))
print(df.shape)
print(df.info())
print(df.describe())
zones=pd.read_csv(r"C:\Users\Shubham Chouhan\OneDrive\Desktop\analysis\data\raw\taxi_zone_lookup.csv",on_bad_lines='skip')
print(zones.head(3))