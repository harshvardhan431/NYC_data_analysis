import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from src.logger_config import setup_logger
import logging
logger=setup_logger(__name__)



def run_analysis(df:pd.DataFrame)->pd.DataFrame:
    try:
        logger.info("analysis is be hit")
        df=bivariate_numerical_numerical(df)
        df=time_analysis(df)
        df=mulitvariate_analysis(df)
        df=bivariate_categorical_analysis(df)
        df=categorical_analysis(df)
    except Exception as e:
        logger.error(f"error occured is {e}",exc_info=True)
    return df

def passenger_analysis(df:pd.DataFrame)->pd.DataFrame:
    print(df["passenger_count"].describe())
    plt.figure(figsize=(8,5)) 
    sns.countplot(x="passenger_count",data=df)
    plt.title("distribution of passenger")
    plt.show()
    return df

def trip_distance_analysis(df:pd.DataFrame)->pd.DataFrame:
    print(df["trip_distance"].describe())
    plt.figure(figsize=(8,5))
    sns.histplot(df["trip_distance"],bins=50)
    plt.title("distribution of trip_distance")
    plt.xlabel("trip distance")
    plt.ylabel("count")
    plt.show()
    return df 

def total_amount_analysis(df:pd.DataFrame)->pd.DataFrame:
    print(df["total_amount"].describe())
    plt.figure(figsize=(8,5))
    sns.histplot(df["total_amount"],bins=50)
    plt.title("distribution of total amount")
    plt.xlabel("total_amount")
    plt.ylabel("count")
    plt.show()
    return df 

#summary of numerical data
def numerical_summary(df:pd.DataFrame,numerical_cols:list)->pd.DataFrame:
    summary=df[numerical_cols].describe().T
    summary['median']=df[numerical_cols].median()
    summary["iqr"]=summary["75%"]-summary["25%"]
    summary["skewness"]=df[numerical_cols].skew()
    summary["kurtosis"]=df[numerical_cols].kurt()
    print("summary of numerical data")
    return summary 

#box plot representation for numerical cols
def box_representation(df:pd.DataFrame,numerical_cols:list)->pd.DataFrame:
    
    for cols in numerical_cols:
        if cols=="trip_distance":
            plt.figure(figsize=(12,4))
            plt.subplot(1,3,1)
            sns.histplot(df[cols],kde=True,bins=50)
            plt.title(f"histogram of trip_distance")
        else:
          plt.figure(figsize=(12,4))
          plt.subplot(1,3,1)
          sns.histplot(df[cols],kde=True)#you get a curve to know whether it is skewed or not 
          plt.title(f"histogram of {cols}")

        plt.subplot(1,3,2)
        sns.boxplot(y=df[cols])
        plt.title(f"boxplot of {cols}")

        plt.subplot(1,3,3)
        sns.kdeplot(y=df[cols],fill=True)#kdeplot draws the bars and then gives a curve for comparison 
        plt.title(f"density plot  of {cols}")
        plt.tight_layout()
        plt.show()

    return df


def  categorical_analysis(df:pd.DataFrame)->pd.DataFrame:
    cat_cols=["ratecodeid","vendorid","payment_type"]
    logger.info("categorical analysiss route is being hit ")
    for cols in cat_cols:
        plt.figure(figsize=(6,4))
        sns.countplot(x=cols,data=df,order=df[cols].value_counts().index)
        plt.title(f"bar chart of {cols}")
        plt.show()
    return df



#bivariate analysis 
def bivariate_numerical_numerical(df:pd.DataFrame)->pd.DataFrame:
    sample=df.sample(min(20000,len(df)),random_state=42)#always right minimum here so it is easy if there are less than 20 thosuhand rows 
    plt.figure(figsize=(8,5))
    plt.subplot(1,3,1)
    sns.scatterplot(x="trip_distance",y="total_amount",data=sample,alpha=0.1)
    plt.title("trip distance vs total_amount")
    print(df[["trip_distance","total_amount"]].corr())#this always defualt to pearson's correlation which may not be correct always


    plt.subplot(1,3,2)
    sns.scatterplot(x="passenger_count",y="total_amount",data=sample,alpha=0.1)
    plt.title("passenger counts vs total amounts")
    print(df[["passenger_count","total_amount"]].corr())

    plt.subplot(1,3,3)
    sns.scatterplot(x="passenger_count",y="trip_distance",data=sample,alpha=0.1)
    plt.title("passenger count vs trip distance")
    print(df[["passenger_count","trip_distance"]].corr())

    return df 

#categorical vs numerical 
# bivariate analysis - categorical vs numerical
def bivariate_categorical_analysis(df: pd.DataFrame,target: str = "total_amount") -> pd.DataFrame:
    logger.info("categorical analysis route is being loaded")
    bi_cals=["payment_type","pickup_hour","pickup_dayofweek"]
    for cols in bi_cals:
        plt.figure(figsize=(14, 4))

        # boxplot: distribution of target across categories
        plt.subplot(1, 3, 1)
        sns.boxplot(x=cols, y=target, data=df)
        plt.title(f"{target} by {cols}")
        plt.xticks(rotation=45)

        # barplot: mean of target per category
        plt.subplot(1, 3, 2)
        sns.barplot(x=cols, y=target, data=df, estimator="mean", errorbar=None)
        plt.title(f"mean {target} by {cols}")
        plt.xticks(rotation=45)

        # countplot: frequency of each category
        plt.subplot(1, 3, 3)
        sns.countplot(x=cols, data=df)
        plt.title(f"count of {cols}")
        plt.xticks(rotation=45)

        plt.tight_layout()
        plt.show()

        # quick numeric summary per category
        print(f"\nsummary of {target} grouped by {cols}")
        print(df.groupby(cols)[target].agg(["mean", "median", "std", "count"]))

    return df


#multivariate analysis   hours ,trip_distance,fare
def mulitvariate_analysis(df:pd.DataFrame)->pd.DataFrame:
    numerical_cols = ["passenger_count", "trip_distance", "fare_amount", 
                   "tip_amount", "total_amount", "trip_duration_minutes"]
    corr = df[numerical_cols].corr()

    plt.figure(figsize=(8,6))
    sns.heatmap(corr, annot=True, cmap="coolwarm", fmt=".2f")
    plt.title("Correlation heatmap of numerical trip variables")
    plt.show()

    pivot = df.pivot_table(
    index="pickup_hour", 
    columns="payment_type", 
    values="total_amount", 
    aggfunc="mean"
    )
    print(pivot)

    pivot.plot(kind="line", figsize=(10,5))
    plt.title("Average fare by hour, split by payment type")
    plt.xlabel("Pickup hour")
    plt.ylabel("Average total amount")
    plt.show()

    pivot2 = df.pivot_table(
    index="pickup_hour",
    columns="pickup_borough",
    values="total_amount",
    aggfunc="mean"
    )
    pivot2.plot(figsize=(12,6))
    plt.title("Average fare by hour, across boroughs")
    plt.show()
    return df



#time series analysis
def time_analysis(df:pd.DataFrame)->pd.DataFrame:
    logger.info("time series analysis route is hit")
    df["hour"]=df["tpep_dropoff_datetime"].dt.hour
    df["day"]=df["tpep_dropoff_datetime"].dt.day

    hour_count=df.groupby("hour").size()
    print(hour_count)
    day_count=df.groupby("day").size()
    print(day_count)

    hour_count.plot(kind="line",figsize=(10,5))
    plt.xlabel("hour")
    plt.ylabel("no of trips per hour")
    plt.title("trips per hour")
    plt.show()

    day_count.plot(kind="line",figsize=(10,5))
    plt.xlabel("day")
    plt.ylabel("no of trips per day")
    plt.title("trips per day")
    plt.show()
    return df


    






    



    
