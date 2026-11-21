import pandas as pd
import pytest

from src.cleaning import clean


def make_df(rows):
    return pd.DataFrame(rows, columns=["country_name", "country_code", "indicator_name",
                                       "indicator_code", "debt"])


ROW = ("China", "CHN", "PPG, bonds (AMT, current US$)", "DT.AMT.PBND.CD", 100.0)


def test_strips_spaces_and_removes_duplicates():
    df = make_df([ROW, ("China  ", "CHN", ROW[2], ROW[3], 100.0)])
    out, report = clean(df)
    assert len(out) == 1
    assert report["duplicates_removed"] == 1
    assert out.loc[0, "country_name"] == "China"


def test_drops_missing_debt():
    df = make_df([ROW, ("India", "IND", ROW[2], ROW[3], None)])
    out, report = clean(df)
    assert report["missing_debt_removed"] == 1
    assert list(out["country_code"]) == ["CHN"]


def test_conflicting_values_keep_first():
    df = make_df([ROW, ("China", "CHN", ROW[2], ROW[3], 999.0)])
    out, report = clean(df)
    assert report["conflicting_rows_removed"] == 1
    assert out.loc[0, "debt"] == 100.0


def test_flags_aggregates():
    df = make_df([ROW, ("South Asia", "SAS", ROW[2], ROW[3], 50.0)])
    out, report = clean(df)
    assert out.set_index("country_code").loc["SAS", "is_aggregate"] == 1
    assert report["countries"] == 1


def test_missing_column_raises():
    with pytest.raises(ValueError):
        clean(pd.DataFrame({"country_name": ["China"]}))
