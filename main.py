#%%

from src.load_data import load_raw_data
from src.clean_data import remove_outliers,clean_data
from src.analysis import run_analysis,numerical_summary,box_representation,categorical_analysis
from src.logger_config import setup_logger
import logging
loggger=setup_logger(__name__)

import pandas as pd

df = load_raw_data("data/raw/yellow_tripdata_2026-01.parquet")
print(df.head(3))
print(df.info())
#print(df.isnull().sum())
print(df.describe())
zones=pd.read_csv("data/raw/taxi_zone_lookup.csv")

df=df.merge(zones,left_on="PULocationID",right_on="LocationID",how="left")
df=df.rename(columns={"Zone":"pickup_zone","Borough":"pickup_borough"})
df=df.drop(columns=["LocationID","service_zone"])

df=df.merge(zones,left_on="DOLocationID",right_on="LocationID",how="left")
df=df.rename(columns={"Zone":"dropoff_zone","Borough":"dropoff_borough"})
df=df.drop(columns=["LocationID","service_zone"])
before_count=len(df)
#dupes=df[df.duplicated()]
#print("no of duplicated rows are",dupes)
#dupes_subset = df[df.duplicated(subset=["tpep_pickup_datetime", "tpep_dropoff_datetime", "fare_amount"])]
#print(dupes_subset.shape[0])
#print(df.columns)
"""component_sum = (
    df["fare_amount"] + df["extra"] + df["mta_tax"] + df["tip_amount"] +
    df["tolls_amount"] + df["improvement_surcharge"] +
    df.get("congestion_surcharge", 0) + df.get("airport_fee", 0)
)
lesser=df[df["total_amount"]<component_sum]

print("Rows where total is less than sum of component:", lesser)"""
print(df[df["tip_amount"]<0])
#print(df["payment_type"].unique())

pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
print("after cleaning of data ")
print(df.columns.tolist())
print(df.columns.duplicated().sum())  # should be 0
df=clean_data(df)
print(f"the no of columns are {len(df)}")
#outlier_columns = ["trip_distance","trip_duration_minutes","total_amount"]
"""for col in outlier_columns:
    q1, q3 = df[col].quantile([0.25, 0.75])
    iqr = q3 - q1
    lower, upper = q1 - 1.5*iqr, q3 + 1.5*iqr
    kept = df[(df[col] >= lower) & (df[col] <= upper)]
    print(f"{col}: would keep {len(kept)} / {len(df)} ({len(kept)/len(df)*100:.1f}%)")
df[outlier_columns] = df[outlier_columns].apply(pd.to_numeric, errors='coerce')"""
#df = remove_outliers(df, outlier_columns) this is not suitable strategery here 
numerical_cols=["passenger_count","trip_distance","total_amount"]
cat_cols=["ratecodeid","vendorid","payment_type"]
results=run_analysis(df)
summary=numerical_summary(df,numerical_cols)
print(summary)
box=box_representation(df,numerical_cols)
print(box)
cat_result=categorical_analysis(df,cat_cols)
print(cat_result)
print(f"Before: {before_count}, After: {len(df)}, Removed: {before_count - len(df)} ({(before_count-len(df))/before_count*100:.2f}%)")

print(df.head(3))
print(df.describe())

 # %%
