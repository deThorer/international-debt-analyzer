"""Charts saved to outputs/charts/."""
from pathlib import Path

import matplotlib

matplotlib.use("Agg")  # no display needed
import matplotlib.pyplot as plt  # noqa: E402
import pandas as pd  # noqa: E402

FLOW_LABELS = {"AMT": "Principal repayments", "DIS": "Disbursements", "INT": "Interest payments"}


def _save(fig, path: Path):
    fig.tight_layout()
    fig.savefig(path, dpi=130)
    plt.close(fig)


def top_debtors_chart(df: pd.DataFrame, out_dir: Path):
    df = df.sort_values("naive_total_bn_usd")
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.barh(df["country_name"], df["naive_total_bn_usd"], color="#9bb7d4", label="All indicators (double counts)")
    ax.barh(df["country_name"], df["dedup_total_bn_usd"], color="#2f5d8a", label="Long-term totals only (no double counting)")
    ax.set_xlabel("US$ billion")
    ax.set_title("Top 10 debtor countries")
    ax.legend(loc="lower right", frameon=False)
    ax.spines[["top", "right"]].set_visible(False)
    _save(fig, out_dir / "top10_debtors.png")


def creditor_mix_chart(df: pd.DataFrame, out_dir: Path):
    """Stacked bars: share of long-term debt by creditor class, per flow type."""
    pivot = df.pivot(index="flow_type", columns="creditor", values="pct_of_long_term").fillna(0)
    pivot.index = [FLOW_LABELS.get(i, i) for i in pivot.index]
    colors = ["#2f5d8a", "#9bb7d4", "#e0a458"]
    fig, ax = plt.subplots(figsize=(8.5, 4))
    bottom = None
    for color, col in zip(colors, pivot.columns):
        ax.bar(pivot.index, pivot[col], bottom=bottom, label=col, color=color)
        bottom = pivot[col] if bottom is None else bottom + pivot[col]
    ax.set_ylabel("% of long-term total")
    ax.set_ylim(0, 105)
    ax.set_title("Who the long-term debt is owed to")
    ax.legend(frameon=False, fontsize=8, loc="upper left", bbox_to_anchor=(1.0, 1.0))
    ax.spines[["top", "right"]].set_visible(False)
    _save(fig, out_dir / "creditor_mix.png")


def indicator_coverage_chart(df: pd.DataFrame, out_dir: Path):
    df = df.sort_values("indicator_count")
    fig, ax = plt.subplots(figsize=(7, 6))
    ax.barh(df["indicator_code"], df["indicator_count"], color="#2f5d8a")
    ax.set_xlabel("Number of countries reporting")
    ax.set_title("Indicator coverage")
    ax.spines[["top", "right"]].set_visible(False)
    _save(fig, out_dir / "indicator_coverage.png")
