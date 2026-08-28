# NYC Yellow Taxi Trip Analysis

End-to-end exploratory data analysis project built on NYC Yellow Taxi trip records. This project demonstrates a practical analytics workflow: raw data ingestion, cleaning and validation, geographic enrichment with taxi zone metadata, feature engineering, and exploratory analysis across fare, tipping, trip distance, and pickup behavior.

## Project Overview

The goal of this project is to transform raw NYC taxi trip data into a clean, analysis-ready dataset and use it to investigate operational and customer behavior patterns such as:

- how trip distance relates to total fare
- how payment method affects tipping behavior
- when trip demand peaks by hour and day of week
- how trip patterns vary across pickup and dropoff zones

This project emphasizes both **data analysis** and **analytics engineering practices**, including modular Python code, reproducible file paths, parquet outputs, and pipeline logging.

## Dataset

- **Primary source:** NYC TLC Yellow Taxi Trip Record Data
- **Raw file used:** `yellow_tripdata_2026-01.parquet`
- **Supplementary source:** `taxi_zone_lookup.csv`
- **Purpose of lookup table:** map `PULocationID` and `DOLocationID` to borough and zone names for more interpretable geographic analysis

## What This Project Does

The pipeline:

1. loads raw taxi trip data
2. loads taxi zone lookup data
3. merges pickup and dropoff zone metadata
4. standardizes and cleans the dataset
5. engineers time-based features
6. saves a cleaned parquet output
7. runs exploratory analysis functions for numerical, categorical, and multivariate patterns

## Data Cleaning and Preparation

The cleaning workflow includes:

- column name normalization
- duplicate removal
- timestamp validation and correction when pickup/dropoff values are inconsistent
- correction of negative or invalid monetary fields
- reconciliation of `total_amount` against component fare fields
- creation of `trip_duration` for downstream analysis
- outlier filtering using domain-informed rules rather than a naive IQR-only approach

This approach is designed to preserve realistic NYC taxi behavior, including short urban trips and long-tail higher-value rides such as airport travel.

## Feature Engineering

Additional analysis-ready features include:

- `pickup_hour`
- `pickup_dayofweek`
- `trip_duration`
- pickup and dropoff borough / zone labels
- human-readable payment type labels

These features support temporal, geographic, and behavioral analysis without requiring repeated transformation work in the notebook.

## Analysis Scope

The project covers multiple layers of exploratory data analysis:

### Univariate Analysis
- passenger count distribution
- trip distance distribution
- total fare / total amount distribution

### Categorical Analysis
- frequency patterns across payment type, vendor, and rate code

### Bivariate Analysis
- fare and total amount patterns by payment method
- ride behavior by pickup hour
- ride behavior by day of week
- distance and fare relationships

### Multivariate / Time-Based Analysis
- numerical summaries and distribution comparisons
- time-series patterns in trip volume
- combined trend exploration across temporal and categorical dimensions

## Tech Stack

- **Python**
- **Pandas**
- **NumPy**
- **PyArrow**
- **Matplotlib**
- **Seaborn**
- **Jupyter Notebook**

## Repository Structure

```text
analysis/
├── data/
│   ├── raw/                  # source parquet and taxi zone lookup CSV
│   └── processed/            # cleaned pipeline output
├── notebook/
│   └── eda.ipynb             # charts, exploration, and commentary
├── src/
│   ├── load_data.py          # raw data ingestion
│   ├── clean_data.py         # cleaning and validation logic
│   ├── analysis.py           # EDA and analytical functions
│   └── logger_config.py      # logging configuration
├── config.py                 # shared file paths
├── main.py                   # end-to-end execution script
├── requirements.txt
└── README.md
