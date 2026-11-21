"""Run the SQL files against a tiny hand-made dataset where the answers are known."""
import sqlite3
from pathlib import Path

import pandas as pd
import pytest

from src.cleaning import clean
from src.db import build_database

ROOT = Path(__file__).resolve().parents[1]


@pytest.fixture
def db(tmp_path):
    rows = []
    # values in US$ million. country A: long-term 100 = official 60 + private 30 + PNG 10
    for code, val in [("DLXF", 100), ("OFFT", 60), ("PRVT", 30), ("DPNG", 10)]:
        rows.append(("A", "AAA", "x", f"DT.AMT.{code}.CD", val * 1e6))
    # country B: long-term 50 = official 50
    for code, val in [("DLXF", 50), ("OFFT", 50)]:
        rows.append(("B", "BBB", "x", f"DT.AMT.{code}.CD", val * 1e6))
    rows.append(("South Asia", "SAS", "x", "DT.AMT.DLXF.CD", 1000 * 1e6))  # aggregate, must be ignored
    df = pd.DataFrame(rows, columns=["country_name", "country_code", "indicator_name",
                                     "indicator_code", "debt"])
    cleaned, _ = clean(df)
    return build_database(cleaned, tmp_path / "test.db")


def run(db, name):
    with sqlite3.connect(db) as conn:
        return pd.read_sql_query((ROOT / "sql" / name).read_text(), conn)


def test_country_count_excludes_aggregates(db):
    assert run(db, "01_distinct_countries.sql").iloc[0, 0] == 2


def test_dedup_total_uses_long_term_only(db):
    row = run(db, "03_total_debt.sql").iloc[0]
    assert row["naive_total_million_usd"] == pytest.approx(300)   # 200 (A) + 100 (B)
    assert row["dedup_total_million_usd"] == pytest.approx(150)


def test_creditor_mix_percentages(db):
    mix = run(db, "09_creditor_mix.sql").set_index("creditor")
    # official = (60 + 50) / 150
    assert mix.loc["Official (PPG)", "pct_of_long_term"] == pytest.approx(73.3, abs=0.1)
