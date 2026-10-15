# NYC Yellow Taxi Trip Analysis

End-to-end exploratory data analysis project built on NYC Yellow Taxi trip records. It covers raw data ingestion, cleaning and validation, geographic enrichment with taxi zone metadata, feature engineering, and exploratory analysis of fares, tipping, trip distance, and pickup behavior.

## Project Overview

The goal is to turn raw NYC taxi trip data into a clean, analysis-ready dataset and use it to investigate patterns such as:

- how trip distance relates to total fare
- how payment method affects tipping behavior
- when trip demand peaks by hour and day of week
- how trip patterns vary across pickup and dropoff zones

The project emphasizes both **data analysis** and **analytics engineering practices**: modular Python code, reproducible file paths, parquet outputs, and pipeline logging.

## Tech Stack

- **Python 3.10+**
- **Pandas**, **NumPy**, **PyArrow**
- **Matplotlib**, **Seaborn**
- **Jupyter Notebook** (`ipykernel`)

## Dataset

- **Primary source:** [NYC TLC Yellow Taxi Trip Record Data](https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page)
- **Raw file used:** `yellow_tripdata_2026-01.parquet`
- **Supplementary source:** `taxi_zone_lookup.csv` (also on the TLC page), used to map `PULocationID` and `DOLocationID` to borough and zone names

## Repository Structure

```text
analysis/
├── data/
│   ├── raw/                  # source parquet and taxi zone lookup CSV (you add these)
│   └── processed/            # cleaned pipeline output (created by the pipeline)
├── notebook/
│   └── eda.ipynb             # charts, exploration, and commentary
├── src/
│   ├── load_data.py          # raw data ingestion
│   ├── clean_data.py         # cleaning and validation logic
│   ├── analysis.py           # reusable EDA functions
│   └── logger_config.py      # logging configuration
├── config.py                 # shared file paths
├── main.py                   # end-to-end execution script
├── pipeline.log              # run log (generated)
├── requirements.txt
└── README.md
```

## How to Run

Follow these steps in order.

### Step 1: Install the tools

- [Python 3.10+](https://www.python.org/downloads/)
- [VS Code](https://code.visualstudio.com/)

### Step 2: Install the VS Code extensions

Open VS Code, go to the Extensions tab (`Ctrl+Shift+X`), and install:

| Extension | Why you need it |
|---|---|
| **Python** (Microsoft) | Runs `.py` files and gives you the **Run Cell** buttons for `#%%` cells in `main.py` |
| **Jupyter** (Microsoft) | Opens and runs `eda.ipynb` inside VS Code |

### Step 3: Get the code and install dependencies

```bash
git clone <your-repo-url>
cd analysis
python -m venv venv
venv\Scripts\activate          # Windows
# source venv/bin/activate     # Mac / Linux
pip install -r requirements.txt
```

### Step 4: Add the data

Download the two files from the TLC page and place them here:

```text
data/raw/yellow_tripdata_2026-01.parquet
data/raw/taxi_zone_lookup.csv
```

Also make sure the output folder exists:

```bash
mkdir data/processed
```

### Step 5: Run the pipeline (`main.py`)

Open the **project root folder** in VS Code (not a subfolder), then pick one option.

**Option A: Run the whole script**

```bash
python main.py
```

**Option B: Run it cell by cell**

`main.py` is split into cells using `#%%` markers. With the Python extension installed, each cell shows a **Run Cell** button above it. Run the cells **in order, top to bottom**:

| Cell | What it does |
|---|---|
| `#%% Load data` | Loads the raw parquet and prints a quick overview |
| `#%% Load zones data and merge` | Adds pickup and dropoff borough / zone names |
| `#%%mapping of appropriate payment method` | Converts payment codes to readable labels |
| `#%% before cleaning` | Shows the columns before cleaning |
| `#%% after cleaning` | Runs `clean_data()` and saves the cleaned parquet (this is the slow step) |
| `#%% numerical analysis...` | Runs the numerical and time-series analysis |
| `#%% Eda categorical` | Runs the categorical analysis and prints the rows removed |

You can also click **Run All** at the top of the Interactive Window.

When it finishes you will have:

- `data/processed/cleaned_taxi_data.parquet`
- progress messages in `pipeline.log`

### Step 6: Explore the results (`eda.ipynb`)

The notebook is where the charts and commentary live. **Run `main.py` first**, because the notebook reads the cleaned parquet that the pipeline creates.

1. Open `notebook/eda.ipynb` in VS Code.
2. Click **Select Kernel** (top right) and choose the Python environment you installed the requirements into (`venv`).
3. Click **Run All**, or run one cell at a time with `Shift+Enter`.

**What is a `.ipynb` file?** It is a Jupyter Notebook: a document made of *cells*. Code cells run Python and show their output (tables, charts) right underneath. Markdown cells hold written notes. That is why the charts show up directly in the notebook on GitHub, with no need to run anything.

**Notebook vs scripts:**

| File | Role |
|---|---|
| `main.py` + `src/clean_data.py` | The pipeline: raw data in, cleaned data out, same result every run |
| `src/analysis.py` | Reusable analysis functions |
| `notebook/eda.ipynb` | Loads the cleaned data, calls those functions, shows charts, and explains the findings |

### Troubleshooting

- **`ModuleNotFoundError: src` or `config`**: run from the project root, not from inside `src/` or `notebook/`. In the notebook, add `import sys; sys.path.append("..")` in the first cell.
- **`FileNotFoundError` for `data/raw/...`**: the data files are missing or the working directory is wrong (see Step 4).
- **No output after cleaning**: the cleaning cell has not been run yet. Check `pipeline.log` for `src.clean_data` lines.
- **Cleaning is slow**: expected on a full month of data. It takes about a minute.

## What the Pipeline Does

1. loads raw taxi trip data
2. loads taxi zone lookup data
3. merges pickup and dropoff zone metadata
4. standardizes and cleans the dataset
5. engineers time-based features
6. saves a cleaned parquet output
7. runs exploratory analysis functions for numerical, categorical, and multivariate patterns

## Data Cleaning and Preparation

- column name normalization
- duplicate removal
- timestamp validation and correction when pickup and dropoff values are inconsistent
- correction of negative or invalid monetary fields
- reconciliation of `total_amount` against component fare fields
- creation of `trip_duration` for downstream analysis
- outlier filtering using domain-informed rules rather than a naive IQR-only approach

This preserves realistic NYC taxi behavior, including short urban trips and long-tail higher-value rides such as airport travel.

## Feature Engineering

- `pickup_hour`
- `pickup_dayofweek`
- `trip_duration`
- pickup and dropoff borough / zone labels
- human-readable payment type labels

## Analysis Scope

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

## Key Findings



*Based on NYC Yellow Taxi trips, January 2026.*

**Demand and timing**
- Saturday has the most pickups; Sunday and Monday have the fewest
- Wednesday to Friday generate the highest total fare revenue
- Pickups peak at 5 to 6 PM (hours 17 and 18)
- Early-morning pickups (hours 5 and 6) are few but have the highest total fare per trip, which suggests longer trips such as airport rides
- Trip volume spikes on Jan 10, 15, 24 and 30

**Fares and payments**
- Credit card is the most common payment type (X% of trips)
- Pickups in Manhattan have lower average fares than other boroughs
- EWR (Newark Airport) has the highest average fare ($X)

**Trips and tips**
- Most trips carry 1 passenger (X%)
- Short trips under X miles get a higher tip percentage than long trips
- Rate code 1 (standard rate) is the most used, and vendor 2 is the most common vendor