# Data

The raw data is not committed to git (see `.gitignore`).

## Option A: DataCamp extract (included; what the results in the main README use)
`data/raw/international_debt.csv`: 2,357 rows, from the DataCamp project "Analyze International
Debt Statistics". Original source: World Bank, International Debt Statistics
(https://datacatalog.worldbank.org), licensed CC BY 4.0.

Columns:

| column | type | description |
|---|---|---|
| country_name | text | country (may include a few aggregates) |
| country_code | text | ISO3 code |
| indicator_name | text | description of the debt series |
| indicator_code | text | World Bank series code, e.g. `DT.AMT.DLXF.CD` |
| debt | float | value in current US$ |

## Option B: World Bank API
```bash
python scripts/fetch_worldbank.py --year 2015
```
Writes `data/raw/international_debt_wb_2015.csv` with the same columns plus `is_aggregate`.
Source: World Bank International Debt Statistics (source id 6).

## Option C: synthetic sample
```bash
python scripts/make_sample_data.py
```
Random numbers in the right format, with a few duplicates, missing values and padded
names added on purpose to test the cleaning step. **Not real data.**
