"""
Indicator metadata for the World Bank International Debt Statistics (IDS) subset.

The 25 indicators are flows (repayments, disbursements, interest), NOT the stock
of debt. They are also hierarchical, e.g.

    long-term (DLXF) = public & publicly guaranteed (PPG) + private non-guaranteed (DPNG)
    PPG              = official creditors (OFFT) + private creditors (PRVT)
    OFFT             = bilateral (BLAT) + multilateral (MLAT)
    PRVT             = bonds (PBND) + commercial banks (PCBK) + other private (PROP)

So adding up every indicator counts the same dollar several times. LEVELS below
lets the SQL compute a de-duplicated total as well.
"""

# code -> human readable name (as they appear in the IDS dataset)
INDICATORS = {
    # Principal repayments (AMT)
    "DT.AMT.BLAT.CD": "Principal repayments on external debt, bilateral (AMT, current US$)",
    "DT.AMT.DLXF.CD": "Principal repayments on external debt, long-term (AMT, current US$)",
    "DT.AMT.DPNG.CD": "Principal repayments on external debt, private nonguaranteed (PNG) (AMT, current US$)",
    "DT.AMT.MLAT.CD": "Principal repayments on external debt, multilateral (AMT, current US$)",
    "DT.AMT.OFFT.CD": "Principal repayments on external debt, official creditors (AMT, current US$)",
    "DT.AMT.PBND.CD": "PPG, bonds (AMT, current US$)",
    "DT.AMT.PCBK.CD": "PPG, commercial banks (AMT, current US$)",
    "DT.AMT.PROP.CD": "PPG, other private creditors (AMT, current US$)",
    "DT.AMT.PRVT.CD": "PPG, private creditors (AMT, current US$)",
    # Disbursements (DIS)
    "DT.DIS.BLAT.CD": "Disbursements on external debt, bilateral (DIS, current US$)",
    "DT.DIS.DLXF.CD": "Disbursements on external debt, long-term (DIS, current US$)",
    "DT.DIS.MLAT.CD": "Disbursements on external debt, multilateral (DIS, current US$)",
    "DT.DIS.OFFT.CD": "PPG, official creditors (DIS, current US$)",
    "DT.DIS.PCBK.CD": "PPG, commercial banks (DIS, current US$)",
    "DT.DIS.PROP.CD": "PPG, other private creditors (DIS, current US$)",
    "DT.DIS.PRVT.CD": "PPG, private creditors (DIS, current US$)",
    # Interest payments (INT)
    "DT.INT.BLAT.CD": "Interest payments on external debt, bilateral (INT, current US$)",
    "DT.INT.DLXF.CD": "Interest payments on external debt, long-term (INT, current US$)",
    "DT.INT.DPNG.CD": "Interest payments on external debt, private nonguaranteed (PNG) (INT, current US$)",
    "DT.INT.MLAT.CD": "Interest payments on external debt, multilateral (INT, current US$)",
    "DT.INT.OFFT.CD": "PPG, official creditors (INT, current US$)",
    "DT.INT.PBND.CD": "PPG, bonds (INT, current US$)",
    "DT.INT.PCBK.CD": "PPG, commercial banks (INT, current US$)",
    "DT.INT.PROP.CD": "PPG, other private creditors (INT, current US$)",
    "DT.INT.PRVT.CD": "PPG, private creditors (INT, current US$)",
}

# Position of each series in the hierarchy (the middle part of the code, e.g. "DLXF").
#   level 1 = long-term total (DLXF)            -> summing only these avoids double counting
#   level 2 = PPG official (OFFT), PPG private (PRVT), private non-guaranteed (DPNG)
#   level 3 = bilateral, multilateral, bonds, commercial banks, other private
# Note: not every flow type has every child (e.g. no DIS.PBND / DIS.DPNG in this subset),
# so summing the lowest level would UNDER-count. The level-1 total is the safe choice.
LEVELS = {"DLXF": 1, "OFFT": 2, "PRVT": 2, "DPNG": 2,
          "BLAT": 3, "MLAT": 3, "PBND": 3, "PCBK": 3, "PROP": 3}

CREDITOR = {"DLXF": "All long-term", "OFFT": "Official (PPG)", "PRVT": "Private (PPG)",
            "DPNG": "Private non-guaranteed", "BLAT": "Bilateral", "MLAT": "Multilateral",
            "PBND": "Bonds", "PCBK": "Commercial banks", "PROP": "Other private"}

FLOW_TYPES = {"AMT": "Principal repayment", "DIS": "Disbursement", "INT": "Interest payment"}
