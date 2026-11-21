"""Build the SQLite database from the cleaned dataframe."""
import sqlite3
from pathlib import Path

import pandas as pd

from src.indicators import CREDITOR, INDICATORS, LEVELS

ROOT = Path(__file__).resolve().parents[1]
DB_PATH = ROOT / "data/processed/international_debt.db"


def indicator_lookup() -> pd.DataFrame:
    rows = []
    for code, name in INDICATORS.items():
        part = code.split(".")[2]          # e.g. "DLXF"
        rows.append({
            "indicator_code": code,
            "indicator_name": name,
            "flow_type": code.split(".")[1],   # AMT / DIS / INT
            "level": LEVELS[part],
            "creditor": CREDITOR[part],
        })
    return pd.DataFrame(rows)


def build_database(df: pd.DataFrame, db_path: Path = DB_PATH) -> Path:
    db_path.parent.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(db_path) as conn:
        conn.executescript((ROOT / "sql/schema.sql").read_text())
        # append (not replace) so the constraints in schema.sql are kept
        df.to_sql("international_debt", conn, if_exists="append", index=False)
        indicator_lookup().to_sql("indicators", conn, if_exists="append", index=False)
    return db_path


def run_query(sql: str, db_path: Path = DB_PATH) -> pd.DataFrame:
    with sqlite3.connect(db_path) as conn:
        return pd.read_sql_query(sql, conn)
