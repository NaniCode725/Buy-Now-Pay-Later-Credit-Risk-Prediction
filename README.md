BNPL Credit Risk Prediction

















## Database & SQL

- Designed a 3 table database: bnpl_users (the core BNPL data), national_salary (national income by year), and salary_data (state-level cost of living info).
- Split out national_salary as its own table since the national income number was just repeated across every state row in the original salary file — pulling it out avoids storing the same value over and over.
- salary_data stays on its own without a direct link to bnpl_users, since BNPL only tracks country (not state), so there's no shared key to join them on at that level.
- Built an ERD in Lucidchart showing the tables and the one real connection: national_salary links to bnpl_users by year (pulled from transaction_date).
- Built the database in SQLite using Python (pandas + sqlite3) — loads both CSVs, filters BNPL down to USA only, and writes everything into a bnpl_project.db file.
- Wrote 3 SQL queries:
  - A join comparing each user's income to the national median income for their transaction year
  - A group by/aggregation showing average risk score and default rate per customer segment
  - A having + subquery pulling out customer segments with above-average missed payments