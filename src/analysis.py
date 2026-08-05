import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from src.logger_config import setup_logger
import logging


def run_analysis(df:pd.DataFrame)->pd.DataFrame:
    try:
        logging.info("analysis is be hit")
        df=passenger_analysis(df)
        df=trip_distance_analysis(df)
        df=total_amount_analysis(df)
        df=bivariate_numerical_numerical(df)
    except Exception as e:
        logging.error(f"error occured is {e}",exec_info=True)
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
        plt.figure(figsize=(12,4))
        plt.subplot(1,3,1)
        sns.histplot(df[cols],kde=True)
        plt.title(f"histogram of {cols}")

        plt.subplot(1,3,2)
        sns.boxplot(y=df[cols])
        plt.title(f"boxplot of {cols}")

        plt.subplot(1,3,3)
        sns.kdeplot(y=df[cols],fill=True)
        plt.title(f"density plot  of {cols}")
        plt.tight_layout()
        plt.show()

    return df


def  categorical_analysis(df:pd.DataFrame,cat_cols:list)->pd.DataFrame:
    logging.info("categorical analysiss route is being hit ")
    for cols in cat_cols:
        plt.figure(figsize=(6,4))
        sns.countplot(x=cols,data=df,order=df[cols].value_counts().index)
        plt.title(f"bar chart of {cols}")
        plt.show()
    return df



#bivariate analysis 
def bivariate_numerical_numerical(df:pd.DataFrame)->pd.DataFrame:
    sample=df.sample(20000,random_state=42)
    plt.figure(figsize=(8,5))
    plt.subplot(1,3,1)
    sns.scatterplot(x="trip_distance",y="total_amount",data=sample,alpha=0.3)
    plt.title("trip distance vs total_amount")
    print(df[["trip_distance","total_amount"]].corr())

    plt.subplot(1,3,2)
    sns.scatterplot(x="passenger_count",y="total_amount",data=sample,alpha=0.3)
    plt.title("passenger counts vs total amounts")
    print(df[["passenger_count","total_amount"]].corr())

    plt.subplot(1,3,3)
    sns.scatterplot(x="passenger_count",y="trip_distance",data=sample,alpha=0.3)
    plt.title("passenger count vs trip distance")
    print(df[["passenger_count","trip_distance"]].corr())

    return df 





    



    
