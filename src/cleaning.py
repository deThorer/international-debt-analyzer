"""
Data cleaning + validation for the international debt CSV.

Each check records what it found in a report dict so we can print it and
save it with the results (reports/cleaning_report.md). Nothing is dropped
silently.
"""
import pandas as pd

from src.indicators import INDICATORS

EXPECTED_COLUMNS = ["country_name", "country_code", "indicator_name", "indicator_code", "debt"]

# Codes that are regions / income groups rather than countries.
# fetch_worldbank.py also gives an is_aggregate column; this list is the fallback.
KNOWN_AGGREGATES = {
    "SAS", "EAS", "ECA", "LAC", "MNA", "SSA", "LDC", "IDX", "IDA", "IBD", "IDB",
    "LMY", "LIC", "LMC", "MIC", "UMC", "TEC", "TLA", "TMN", "TSA", "TSS", "WLD",
}


def clean(df: pd.DataFrame):
    report = {"rows_in": len(df)}
    df = df.copy()

    # 1. column names
    df.columns = [c.strip().lower() for c in df.columns]
    missing_cols = [c for c in EXPECTED_COLUMNS if c not in df.columns]
    if missing_cols:
        raise ValueError(f"input file is missing columns: {missing_cols}")

    # 2. whitespace in text columns (e.g. "China  ")
    text_cols = ["country_name", "country_code", "indicator_name", "indicator_code"]
    before = df[text_cols].copy()
    for col in text_cols:
        df[col] = df[col].astype("string").str.strip()
    report["cells_trimmed"] = int((before != df[text_cols]).sum().sum())

    # 3. debt must be numeric
    df["debt"] = pd.to_numeric(df["debt"], errors="coerce")

    # 4. exact duplicates (done after trimming so "China  " == "China")
    dup_mask = df.duplicated(keep="first")
    report["duplicates_removed"] = int(dup_mask.sum())
    df = df[~dup_mask]

    # 5. same country + indicator twice with different values -> conflict, keep the first
    key_dup = df.duplicated(subset=["country_code", "indicator_code"], keep="first")
    report["conflicting_rows_removed"] = int(key_dup.sum())
    df = df[~key_dup]

    # 6. missing debt values
    report["missing_debt_removed"] = int(df["debt"].isna().sum())
    df = df.dropna(subset=["debt"])

    # 7. negative values should not exist for these flow series
    report["negative_debt_rows"] = int((df["debt"] < 0).sum())

    # 8. unknown indicator codes
    unknown = sorted(set(df["indicator_code"]) - set(INDICATORS))
    report["unknown_indicator_codes"] = unknown

    # 9. one name per code (both for indicators and countries)
    report["indicator_codes_with_multiple_names"] = int(
        (df.groupby("indicator_code")["indicator_name"].nunique() > 1).sum())
    report["country_codes_with_multiple_names"] = int(
        (df.groupby("country_code")["country_name"].nunique() > 1).sum())

    # 10. flag aggregates instead of deleting them
    if "is_aggregate" in df.columns:
        df["is_aggregate"] = df["is_aggregate"].fillna(0).astype(int)
    else:
        df["is_aggregate"] = df["country_code"].isin(KNOWN_AGGREGATES).astype(int)
    report["aggregate_entities"] = sorted(df.loc[df["is_aggregate"] == 1, "country_name"].unique())

    df = df[EXPECTED_COLUMNS + ["is_aggregate"]].reset_index(drop=True)
    report["rows_out"] = len(df)
    report["countries"] = int(df.loc[df["is_aggregate"] == 0, "country_code"].nunique())
    report["indicators"] = int(df["indicator_code"].nunique())
    return df, report


def report_to_markdown(report: dict, source_file: str) -> str:
    lines = ["# Data cleaning report", "", f"Source file: `{source_file}`", "",
             "| Check | Result |", "|---|---|"]
    for key, value in report.items():
        if isinstance(value, list):
            value = ", ".join(value) if value else "none"
        lines.append(f"| {key.replace('_', ' ')} | {value} |")
    return "\n".join(lines) + "\n"
