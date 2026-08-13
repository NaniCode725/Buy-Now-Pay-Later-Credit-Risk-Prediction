import sqlite3
import pandas as pd


BNPL = pd.read_csv('../Data/Buy_Now_Pay_Later_BNPL_CreditRisk_Dataset.csv')
Salary = pd.read_csv('../Data/usa_col_salary_longitudinal_2010_2024.csv')

bnpl_usa = BNPL[BNPL['location'] == 'USA'].copy()
bnpl_usa['monthly_income'] = bnpl_usa['monthly_income'].astype(int)

national_salary = Salary[['year', 'national_median_gross_usd_monthly']].drop_duplicates()

salary_data = Salary[['year', 'state', 'cost_of_living_index',
                       'median_salary_gross_usd_monthly',
                       'median_salary_net_usd_monthly',
                       'salary_to_national_ratio']]

conn = sqlite3.connect("bnpl_project.db")

bnpl_usa.to_sql('bnpl_users', conn, if_exists='replace', index=False)
national_salary.to_sql('national_salary', conn, if_exists='replace', index=False)
salary_data.to_sql('salary_data', conn, if_exists='replace', index=False)

print("Database built: bnpl_project.db")
print("Tables created: bnpl_users, national_salary, salary_data")

conn.close()