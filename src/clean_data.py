import pandas as pd
from src.logger_config import setup_logger
import logging
logger=setup_logger(__name__)

def clean_data(df:pd.DataFrame)->pd.DataFrame:
    try:
        print("before cleaning len is ",len(df))
        df=clean_heading(df)
        df=drop_duplicates(df)
        df=swap_date(df)
        df=clean_tip_extra_toll(df)
        df=check_total_amount(df)
        df=add_trip_duration(df)
        df=remove_amounts_outliers(df)
        df=clean_trip_distance(df)
        logging.info("cleaned  data")
        print("after cleaning length is ",len(df))
        return df
    except MemoryError:
        logger.error(f"memory error restart the kernel {e}")
    except Exception as e:
        logger.error(f"error occured {e}")
        raise RuntimeError(f"error occured {e}")


def drop_duplicates(df:pd.DataFrame)->pd.DataFrame:
    logger.info("drop duplicated function is hit")
    before=len(df)
    df=df.drop_duplicates()
    after=len(df)
    print(f"the rows are reduced from {before} to {after} after removing duplicates")
    return df

def clean_heading(df:pd.DataFrame)->pd.DataFrame:
    df.columns=df.columns.str.strip().str.lower().str.replace(" ","_")
    
    logger.info("columns cleaned ")
    return df

def swap_date(df:pd.DataFrame)->pd.DataFrame:
    bad_dates=df["tpep_pickup_datetime"]>df["tpep_dropoff_datetime"]
    if bad_dates.any():
        df.loc[bad_dates,["tpep_pickup_datetime","tpep_dropoff_datetime"]]=\
            df.loc[bad_dates,["tpep_dropoff_datetime","tpep_pickup_datetime"]].values
        
        logger.info("dates are swapped ")
    return df

def check_total_amount(df:pd.DataFrame)->pd.DataFrame:
    component_sum = (
    df["fare_amount"] + df["extra"] + df["mta_tax"] + df["tip_amount"] +
    df["tolls_amount"] + df["improvement_surcharge"] +
    df.get("congestion_surcharge", 0) + df.get("airport_fee", 0)+df.get("cbd_congestion_fee",0)
    )
    lesser=df["total_amount"]<component_sum
    if lesser.any():
        df.loc[lesser,["total_amount"]]=component_sum[lesser]#here it fetches the rows with lesser condition and then we see that it makes them qual to sum using lesser as an index
        logger.info("the amount is replaced correctly")

    return df

def clean_tip_extra_toll(df: pd.DataFrame) -> pd.DataFrame:
    logger.info("cleaning of tip, extra, toll, and tax amounts")

    df.loc[df["tip_amount"] < 0, "tip_amount"] = 0
    df.loc[df["extra"] < 0, "extra"] = 0
    df.loc[df["tolls_amount"] < 0, "tolls_amount"] = 0
    df.loc[df["congestion_surcharge"] < 0, "congestion_surcharge"] = 0
    df.loc[df["cbd_congestion_fee"] < 0, "cbd_congestion_fee"] = 0
    df.loc[df["mta_tax"] < 0, "mta_tax"] = 0
    df.loc[df["improvement_surcharge"]<0,"improvement_surcharge"]=0

    return df


def add_trip_duration(df: pd.DataFrame) -> pd.DataFrame:
    logger.info("trip_duration column is added for future use")
    df["tpep_pickup_datetime"] = pd.to_datetime(df["tpep_pickup_datetime"], errors='coerce')
    df["tpep_dropoff_datetime"] = pd.to_datetime(df["tpep_dropoff_datetime"], errors='coerce')
    df["trip_duration_minutes"] = (
        df["tpep_dropoff_datetime"] - df["tpep_pickup_datetime"]
    ).dt.total_seconds() / 60
    return df



def remove_outliers(df:pd.DataFrame,columns:list,multiplier:float=1.5)->pd.DataFrame:
    logger.info("cleaning of outliers")
    for col in columns:
        q1=df[col].quantile(0.25)
        q3=df[col].quantile(0.75)
        iqr=q3-q1

        lower_bound=q1-multiplier*iqr
        upper_bound=q3+multiplier*iqr

        df[col] = df[col].clip(lower=lower_bound, upper=upper_bound)#df=df[df[cols]>=lower_bound & df[cols]<=upper_bound] this keeeps only values within boundary range from q1 to q3
        logging.info(f"{col}: capped values outside [{lower_bound:.2f}, {upper_bound:.2f}]")

    return df

def remove_amounts_outliers(df:pd.DataFrame)->pd.DataFrame:
    logger.info("cleaning the outliers from amounts")
    df=df[df["fare_amount"]>-100]
    df=df[df["tolls_amount"]>=0]
    df=df[(df["total_amount"]>-100) & (df["total_amount"]<500)]
    return df

def clean_trip_distance(df:pd.DataFrame)->pd.DataFrame:
    logger.info("cleaning trip_distance")
    df=df[(df["trip_distance"]>0)&(df["trip_distance"]<300)]
    return df




    




