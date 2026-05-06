# Technical Documentation: COVID-19 Data Science Project

## Data Pipeline Details

### 1. Data Acquisition (`analysis/data_processing.py`)
- **Source**: Our World in Data (OWID) COVID-19 Dataset.
- **Method**: Automated HTTPS request with fallback to GitHub mirrors.
- **Reasoning**: OWID provides the most standardized, multi-variable dataset including health metrics, economic indicators (GDP), and policy indices (Stringency).

### 2. Data Cleaning & Wrangling
- **Datetime Conversion**: Standardizing all date fields for time-series analysis.
- **Null Handling**: 
    - Key metrics (Cases, Deaths, Vax) were filled with `0` for days with no report, as cumulative totals in the raw data are sparse.
    - Rate columns (per million, per hundred) were handled during analysis to avoid skewing global aggregates.
- **Entity Filtering**: 
    - The dataset contains both individual countries and aggregate entities (e.g., "World", "Europe", "High income"). 
    - `iso_code` prefix `OWID_` was used to separate regional aggregates from country-level data to prevent double-counting in charts.

### 3. Exploratory Data Analysis (`analysis/covid_analysis.py`)
- **Library Stack**: `Pandas` for manipulation, `Matplotlib` and `Seaborn` for static visualizations.
- **Analysis Categories**:
    - **Temporal**: Growth and Wave analysis.
    - **Comparative**: Top-N analysis of countries and continents.
    - **Correlative**: Exploring relationships between socio-economic factors (GDP, Age, Life Expectancy) and mortality.
    - **Interventional**: Assessing the impact of Vaccination and Stringency measures.

## Key Insights from the Data
- **The Elderly Gap**: A strong linear correlation exists between the percentage of the population over 65 and total deaths per million, highlighting the primary vulnerability group.
- **Vaccine Efficacy**: Scatter plots show that while high vaccination did not prevent new waves of cases (due to variants), the slope of deaths per million significantly flattened in high-vax nations.
- **The Reporting Paradox**: Higher GDP nations often show higher cumulative mortality. Technical analysis suggests this is due to better diagnostic infrastructure and more transparent reporting compared to lower-income regions.

## Reproducibility
To reproduce this analysis:
1. Run `python analysis/data_processing.py` (requires internet).
2. Run `python analysis/covid_analysis.py`.
3. Check the `report/` and `report/assets/` directories for results.
