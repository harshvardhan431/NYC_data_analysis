#%% Load data

from src.load_data import load_raw_data
from src.clean_data import remove_outliers,clean_data
from src.analysis import run_analysis,numerical_summary,box_representation,categorical_analysis,bivariate_categorical_analysis
from config import RAW_DATA_PATH,ZONE_LOOKUP_PATH,CLEANED_DATA_PATH
from src.logger_config import setup_logger
import logging
logger=setup_logger(__name__)

import pandas as pd
#loading of raw data 
df = load_raw_data(RAW_DATA_PATH)
print(df.head(3))
print(df.info())
print(df.isnull().sum())
print(df.describe())
zones=pd.read_csv(ZONE_LOOKUP_PATH)
logger.info("files loaded sucessfully")

#%% Load zones data and merge 
df=df.merge(zones,left_on="PULocationID",right_on="LocationID",how="left")
df=df.rename(columns={"Zone":"pickup_zone","Borough":"pickup_borough"})
df=df.drop(columns=["LocationID","service_zone"])

df=df.merge(zones,left_on="DOLocationID",right_on="LocationID",how="left")
df=df.rename(columns={"Zone":"dropoff_zone","Borough":"dropoff_borough"})
df=df.drop(columns=["LocationID","service_zone"])
before_count=len(df)
logger.info("merged to know proper location ")
#%%mapping of appropriate payment method
payment_map = {1: "Credit Card", 2: "Cash", 3: "No Charge", 4: "Dispute"}
df["payment_type"] = df["payment_type"].map(payment_map)
print(df[df["tip_amount"]<0])
logger.info("mapped the amount type")
#%% before cleaning
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
print("after cleaning of data ")
print(df.columns.tolist())
print(df.columns.duplicated().sum())  # should be 0
#%% after cleaning
df=clean_data(df)
df.to_parquet(CLEANED_DATA_PATH, index=False)
logger.info("data cleaned and cleaned file is added to data folder ")
print(f"the no of columns are {len(df)}")
df["pickup_hour"] = df["tpep_pickup_datetime"].dt.hour
df["pickup_dayofweek"] = df["tpep_pickup_datetime"].dt.day_name()
bi_cals=["payment_type","pickup_hour","pickup_dayofweek"]
numerical_cols=["passenger_count","trip_distance","total_amount"]
cat_cols=["ratecodeid","vendorid","payment_type"]
#%% numerical anlaysis, time series anlaysis,multivariate analysis
logger.info("univaraite ,bivaraite and multivariate analysis is done ")
results=run_analysis(df)
summary=numerical_summary(df,numerical_cols)
print(summary)
box=box_representation(df,numerical_cols)
print(box)
#%% Eda categorical 
cat_result=categorical_analysis(df,cat_cols)
print(cat_result)
print(f"Before: {before_count}, After: {len(df)}, Removed: {before_count - len(df)} ({(before_count-len(df))/before_count*100:.2f}%)")
logger.info("categorical analysis is done ")




# %%
