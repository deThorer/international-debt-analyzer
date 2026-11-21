"""
Download the 25 debt indicators straight from the World Bank API
(International Debt Statistics, source id 6) and save them in the same
5-column format as the DataCamp extract.

    python scripts/fetch_worldbank.py --year 2015
    -> data/raw/international_debt_wb_2015.csv

Uses only the standard library (urllib) so there is nothing extra to install.
Aggregates (regions / income groups) are flagged by the API with
region.id == "NA"; we keep them but mark them, the cleaning step decides.
"""
import argparse
import csv
import json
import sys
import time
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from src.indicators import INDICATORS  # noqa: E402

API = "https://api.worldbank.org/v2"


def get_json(url, retries=3):
    for attempt in range(retries):
        try:
            with urllib.request.urlopen(url, timeout=60) as resp:
                return json.loads(resp.read().decode("utf-8"))
        except Exception as exc:  # network hiccups are common with this API
            print(f"  retry {attempt + 1}/{retries}: {exc}")
            time.sleep(2 * (attempt + 1))
    raise RuntimeError(f"failed to fetch {url}")


def aggregate_codes():
    """ISO3 codes that are aggregates rather than real countries."""
    data = get_json(f"{API}/country?format=json&per_page=400")
    return {c["id"] for c in data[1] if c["region"]["id"] == "NA"}


def fetch_indicator(code, year):
    url = f"{API}/country/all/indicator/{code}?source=6&date={year}&format=json&per_page=20000"
    data = get_json(url)
    if len(data) < 2 or data[1] is None:
        return []
    return data[1]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--year", type=int, default=2015)
    args = parser.parse_args()

    out = ROOT / f"data/raw/international_debt_wb_{args.year}.csv"
    aggs = aggregate_codes()
    rows = []
    for i, (code, name) in enumerate(INDICATORS.items(), 1):
        print(f"[{i:2d}/{len(INDICATORS)}] {code}")
        for rec in fetch_indicator(code, args.year):
            if rec["value"] is None:
                continue
            iso3 = rec.get("countryiso3code") or rec["country"]["id"]
            rows.append({
                "country_name": rec["country"]["value"],
                "country_code": iso3,
                "indicator_name": name,
                "indicator_code": code,
                "debt": rec["value"],
                "is_aggregate": int(iso3 in aggs),
            })

    out.parent.mkdir(parents=True, exist_ok=True)
    with open(out, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)
    print(f"wrote {len(rows):,} rows -> {out}")


if __name__ == "__main__":
    main()
