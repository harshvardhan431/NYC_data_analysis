# NYC Yellow Taxi Trip Analysis

Exploratory data analysis of NYC yellow taxi trip data, covering data
cleaning, outlier treatment, and univariate, bivariate, multivariate,
and time-series analysis of fare, tip, and trip patterns.

## Data

- **Source:** NYC TLC Trip Record Data — `yellow_tripdata_2026-01.parquet`
- **Supplementary:** Taxi zone lookup table, used to map `PULocationID` /
  `DOLocationID` to pickup/dropoff borough and zone names

## Project Structure

```
analysis/
├── data/
│   ├── raw/            # original parquet + zone lookup CSV
│   └── processed/      # cleaned_taxi_data.parquet (pipeline output)
├── notebook/
│   └── eda.ipynb        # exploratory analysis, charts, and findings
├── src/
│   ├── load_data.py     # raw data loading
│   ├── clean_data.py    # cleaning, validation, outlier treatment
│   ├── analysis.py       # EDA, bivariate/multivariate, time-series functions
│   └── logger_config.py  # logging setup
├── config.py             # file paths and shared constants
├── main.py                # end-to-end pipeline script
└── requirements.txt
```

## Setup

```bash
pip install -r requirements.txt
python main.py
```

Running `main.py` loads the raw data, cleans it, saves the cleaned
dataset to `data/processed/cleaned_taxi_data.parquet`, and runs the
analysis functions. For the full exploratory walkthrough with charts
and commentary, open `notebook/eda.ipynb`.

## Data Cleaning

Cleaning steps applied, in order:

1. Column name normalization (lowercase, stripped, underscored)
2. Duplicate row removal
3. Pickup/dropoff timestamp validation (swapped where pickup > dropoff)
4. Negative value correction for tip, extra, tolls, tax, and surcharge fields
5. `total_amount` reconciliation against its component fields
6. Trip duration calculation from pickup/dropoff timestamps
7. Outlier treatment:
   - Manual domain-informed bounds were used instead of IQR, since IQR
     removed a large share of legitimate short trips due to the strong
     right-skew in `trip_distance` and `total_amount` (heavy long tail
     from airport/long-haul trips)
   - `fare_amount > -100`, `0 <= tolls_amount`, `-100 < total_amount < 500`
   - `trip_distance` bounded to a realistic range for NYC trips

**Row count impact:** [FILL IN — run the instrumented version of
`clean_data()` to get the before/after count for each step, then
summarize here, e.g. "removed X% total: Y% duplicates, Z% outlier
bounds on trip_distance/amount fields"]

## Analysis

- **Univariate:** distribution of passenger count, trip distance, and
  total fare amount
- **Bivariate:** fare amount vs. payment type, pickup hour, and day of
  week; trip distance vs. fare amount and passenger count
- **Multivariate:** correlation across numerical trip variables;
  fare patterns across combined dimensions (e.g. hour × payment type,
  hour × borough)
- **Time series:** trip volume by hour of day and day of month

## Key Findings

[FILL IN once notebook analysis is finalized — this is the section
recruiters read first. Aim for 3-5 concrete, numbers-backed findings, e.g.:
- "Median trip distance is 1.9 miles; the top 25% of trips exceed 3.87 miles"
- "Credit card trips average X% higher fares than cash trips"
- "Trip volume peaks at [hour] and is lowest at [hour]"
- "[Borough] has the highest average fare, driven by [reason]"]

## Next Steps

- Power BI dashboard for interactive exploration of the cleaned dataset