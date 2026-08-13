import sqlite3

conn = sqlite3.connect("bnpl_project.db")
cursor = conn.cursor()

# --- Query 1: JOIN ---
# Compares each user's monthly income to the national median income
# for the year their transaction happened.
query1 = """
SELECT
    b.user_id,
    b.monthly_income,
    strftime('%Y', b.transaction_date) AS txn_year,
    n.national_median_gross_usd_monthly
FROM bnpl_users b
JOIN national_salary n
    ON strftime('%Y', b.transaction_date) = CAST(n.year AS TEXT)
LIMIT 10;
"""

# --- Query 2: GROUP BY + aggregation ---
# Average risk score and default rate for each customer segment.
query2 = """
SELECT
    customer_segment,
    COUNT(*) AS num_users,
    ROUND(AVG(risk_score), 1) AS avg_risk_score,
    ROUND(AVG(default_flag) * 100, 1) AS default_rate_pct
FROM bnpl_users
GROUP BY customer_segment
ORDER BY avg_risk_score DESC;
"""

# --- Query 3: HAVING + subquery ---
# Finds customer segments whose average missed payments is higher
# than the overall average missed payments across all users.
query3 = """
SELECT
    customer_segment,
    ROUND(AVG(missed_payments), 2) AS avg_missed
FROM bnpl_users
GROUP BY customer_segment
HAVING AVG(missed_payments) > (
    SELECT AVG(missed_payments) FROM bnpl_users
);
"""

for label, query in [
    ("Query 1: JOIN (income vs. national median by year)", query1),
    ("Query 2: GROUP BY (risk & default rate by segment)", query2),
    ("Query 3: HAVING + subquery (above-average missed payments)", query3),
]:
    print(f"\n--- {label} ---")
    for row in cursor.execute(query):
        print(row)

conn.close()
