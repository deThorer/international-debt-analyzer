# Data

The raw data is not committed to git (see `.gitignore`).

## Option A: DataCamp extract (what the results in the main README use)
From the DataCamp project "Analyze International Debt Statistics".
Save it as `data/raw/international_debt.csv`.

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
