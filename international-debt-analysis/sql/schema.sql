-- Schema for the SQLite database built by src/db.py

DROP TABLE IF EXISTS international_debt;
CREATE TABLE international_debt (
    country_name   TEXT    NOT NULL,
    country_code   TEXT    NOT NULL,
    indicator_name TEXT    NOT NULL,
    indicator_code TEXT    NOT NULL,
    debt           REAL    NOT NULL CHECK (debt >= 0),
    is_aggregate   INTEGER NOT NULL DEFAULT 0,
    PRIMARY KEY (country_code, indicator_code)
);

-- Lookup table describing each indicator.
-- flow_type: AMT = principal repayment, DIS = disbursement, INT = interest
-- level    : 1 = long-term total (DLXF), 2 = creditor class, 3 = creditor detail
--            only level 1 can be summed without double counting
DROP TABLE IF EXISTS indicators;
CREATE TABLE indicators (
    indicator_code TEXT PRIMARY KEY,
    indicator_name TEXT NOT NULL,
    flow_type      TEXT NOT NULL,
    level          INTEGER NOT NULL,
    creditor       TEXT    NOT NULL
);

CREATE INDEX idx_debt_indicator ON international_debt (indicator_code);

-- Countries only (aggregates such as "South Asia" removed)
DROP VIEW IF EXISTS countries_debt;
CREATE VIEW countries_debt AS
SELECT * FROM international_debt WHERE is_aggregate = 0;
