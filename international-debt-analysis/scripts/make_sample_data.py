"""
Generate a SYNTHETIC sample of the international debt dataset.

Why this exists: the real file (international_debt.csv) is not committed to
the repo. This script makes a file with the same schema so the pipeline can
be run and tested offline. The numbers are random and mean nothing.

For the real analysis use data/raw/international_debt.csv (see data/README.md).

Usage:
    python scripts/make_sample_data.py            # writes data/raw/international_debt_sample.csv
    python scripts/make_sample_data.py --seed 7
"""
import argparse
import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from src.indicators import INDICATORS  # noqa: E402

# 124 low- and middle-income countries (IDS reporting countries)
COUNTRIES = [
    ("Afghanistan", "AFG"), ("Albania", "ALB"), ("Algeria", "DZA"), ("Angola", "AGO"),
    ("Armenia", "ARM"), ("Azerbaijan", "AZE"), ("Bangladesh", "BGD"), ("Belarus", "BLR"),
    ("Belize", "BLZ"), ("Benin", "BEN"), ("Bhutan", "BTN"), ("Bolivia", "BOL"),
    ("Bosnia and Herzegovina", "BIH"), ("Botswana", "BWA"), ("Brazil", "BRA"), ("Bulgaria", "BGR"),
    ("Burkina Faso", "BFA"), ("Burundi", "BDI"), ("Cabo Verde", "CPV"), ("Cambodia", "KHM"),
    ("Cameroon", "CMR"), ("Central African Republic", "CAF"), ("Chad", "TCD"), ("China", "CHN"),
    ("Colombia", "COL"), ("Comoros", "COM"), ("Congo, Dem. Rep.", "COD"), ("Congo, Rep.", "COG"),
    ("Costa Rica", "CRI"), ("Cote d'Ivoire", "CIV"), ("Djibouti", "DJI"), ("Dominica", "DMA"),
    ("Dominican Republic", "DOM"), ("Ecuador", "ECU"), ("Egypt, Arab Rep.", "EGY"), ("El Salvador", "SLV"),
    ("Eritrea", "ERI"), ("Eswatini", "SWZ"), ("Ethiopia", "ETH"), ("Fiji", "FJI"),
    ("Gabon", "GAB"), ("Gambia, The", "GMB"), ("Georgia", "GEO"), ("Ghana", "GHA"),
    ("Grenada", "GRD"), ("Guatemala", "GTM"), ("Guinea", "GIN"), ("Guinea-Bissau", "GNB"),
    ("Guyana", "GUY"), ("Haiti", "HTI"), ("Honduras", "HND"), ("India", "IND"),
    ("Indonesia", "IDN"), ("Iran, Islamic Rep.", "IRN"), ("Jamaica", "JAM"), ("Jordan", "JOR"),
    ("Kazakhstan", "KAZ"), ("Kenya", "KEN"), ("Kosovo", "XKX"), ("Kyrgyz Republic", "KGZ"),
    ("Lao PDR", "LAO"), ("Lebanon", "LBN"), ("Lesotho", "LSO"), ("Liberia", "LBR"),
    ("Madagascar", "MDG"), ("Malawi", "MWI"), ("Maldives", "MDV"), ("Mali", "MLI"),
    ("Mauritania", "MRT"), ("Mauritius", "MUS"), ("Mexico", "MEX"), ("Moldova", "MDA"),
    ("Mongolia", "MNG"), ("Montenegro", "MNE"), ("Morocco", "MAR"), ("Mozambique", "MOZ"),
    ("Myanmar", "MMR"), ("Nepal", "NPL"), ("Nicaragua", "NIC"), ("Niger", "NER"),
    ("Nigeria", "NGA"), ("North Macedonia", "MKD"), ("Pakistan", "PAK"), ("Papua New Guinea", "PNG"),
    ("Paraguay", "PRY"), ("Peru", "PER"), ("Philippines", "PHL"), ("Russian Federation", "RUS"),
    ("Rwanda", "RWA"), ("Samoa", "WSM"), ("Sao Tome and Principe", "STP"), ("Senegal", "SEN"),
    ("Serbia", "SRB"), ("Sierra Leone", "SLE"), ("Solomon Islands", "SLB"), ("Somalia", "SOM"),
    ("South Africa", "ZAF"), ("South Asia", "SAS"), ("Sri Lanka", "LKA"), ("St. Lucia", "LCA"),
    ("St. Vincent and the Grenadines", "VCT"), ("Sudan", "SDN"), ("Syrian Arab Republic", "SYR"),
    ("Tajikistan", "TJK"), ("Tanzania", "TZA"), ("Thailand", "THA"), ("Timor-Leste", "TLS"),
    ("Togo", "TGO"), ("Tonga", "TON"), ("Tunisia", "TUN"), ("Turkey", "TUR"),
    ("Turkmenistan", "TKM"), ("Uganda", "UGA"), ("Ukraine", "UKR"), ("Uzbekistan", "UZB"),
    ("Vanuatu", "VUT"), ("Venezuela, RB", "VEN"), ("Vietnam", "VNM"), ("Yemen, Rep.", "YEM"),
    ("Zambia", "ZMB"), ("Zimbabwe", "ZWE"), ("Least developed countries: UN classification", "LDC"),
    ("IDA only", "IDX"),
]
# NOTE: World Bank downloads often mix regional/income aggregates (e.g. "South Asia",
# "IDA only") in with countries. A few are kept here on purpose so the cleaning step
# has to detect them.

BIG_ECONOMIES = {"CHN": 60, "BRA": 45, "RUS": 42, "IND": 38, "MEX": 35, "IDN": 33,
                 "TUR": 30, "KAZ": 15, "UKR": 12, "ZAF": 12, "THA": 10, "COL": 10}

# parent -> children (same hierarchy for each flow type, where the series exist)
HIERARCHY = {
    "OFFT": ["BLAT", "MLAT"],
    "PRVT": ["PBND", "PCBK", "PROP"],
}


def country_scale(code, rng):
    base = BIG_ECONOMIES.get(code, rng.lognormal(mean=0.3, sigma=0.9))
    return base * 1e8


def build_country_rows(name, code, rng):
    scale = country_scale(code, rng)
    rows = []
    for flow, flow_mult in [("AMT", 1.0), ("DIS", 1.1), ("INT", 0.3)]:
        leaf = {}
        for child in ["BLAT", "MLAT", "PBND", "PCBK", "PROP"]:
            leaf[child] = scale * flow_mult * rng.gamma(2.0, 0.5)
        dpng = scale * flow_mult * rng.gamma(2.0, 0.8)

        values = dict(leaf)
        values["OFFT"] = leaf["BLAT"] + leaf["MLAT"]
        values["PRVT"] = leaf["PBND"] + leaf["PCBK"] + leaf["PROP"]
        values["DPNG"] = dpng
        values["DLXF"] = values["OFFT"] + values["PRVT"] + dpng

        for part, val in values.items():
            ind_code = f"DT.{flow}.{part}.CD"
            if ind_code not in INDICATORS:
                continue
            rows.append((name, code, INDICATORS[ind_code], ind_code, round(val, 1)))
    return rows


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--out", default=str(ROOT / "data/raw/international_debt_sample.csv"))
    args = parser.parse_args()

    rng = np.random.default_rng(args.seed)
    rows = []
    for name, code in COUNTRIES:
        rows.extend(build_country_rows(name, code, rng))

    df = pd.DataFrame(rows, columns=["country_name", "country_code", "indicator_name",
                                     "indicator_code", "debt"])

    # Not every country reports every series -> drop ~5% of non-core rows at random
    core = df["indicator_code"].str.contains("DLXF|OFFT")
    drop = (~core) & (rng.random(len(df)) < 0.05)
    df = df[~drop].copy()

    # Inject a little dirt so the cleaning step has real work to do
    dirty = df.sample(6, random_state=args.seed)
    df = pd.concat([df, dirty])                                   # exact duplicates
    idx = df.sample(4, random_state=args.seed + 1).index
    df.loc[idx, "debt"] = np.nan                                  # missing values
    df.loc[df.sample(3, random_state=args.seed + 2).index, "country_name"] += "  "  # stray spaces

    df = df.sample(frac=1, random_state=args.seed).reset_index(drop=True)
    Path(args.out).parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(args.out, index=False)
    print(f"[synthetic] wrote {len(df):,} rows, {df['country_code'].nunique()} countries -> {args.out}")


if __name__ == "__main__":
    main()
