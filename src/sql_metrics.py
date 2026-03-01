import sqlite3
import pandas as pd

DB_PATH = "data/processed/jobs.db"

QUERIES = {
    "Top 10 job titles": """
        SELECT job_title, COUNT(*) AS n
        FROM jobs
        GROUP BY job_title
        ORDER BY n DESC
        LIMIT 10;
    """,
    "Salary by experience level": """
        SELECT experience_level,
               ROUND(AVG(salary_in_usd), 0) AS avg_salary_usd,
               ROUND(MIN(salary_in_usd), 0) AS min_salary_usd,
               ROUND(MAX(salary_in_usd), 0) AS max_salary_usd,
               COUNT(*) AS n
        FROM jobs
        GROUP BY experience_level
        ORDER BY avg_salary_usd DESC;
    """,
    "Remote ratio distribution (%)": """
        SELECT remote_ratio,
               ROUND(100.0 * COUNT(*) / (SELECT COUNT(*) FROM jobs), 2) AS pct,
               COUNT(*) AS n
        FROM jobs
        GROUP BY remote_ratio
        ORDER BY remote_ratio;
    """,
    "Top 10 locations": """
        SELECT company_location, COUNT(*) AS n
        FROM jobs
        GROUP BY company_location
        ORDER BY n DESC
        LIMIT 10;
    """,
    "Top titles in US only": """
        SELECT job_title, COUNT(*) AS n
        FROM jobs
        WHERE company_location = 'US'
        GROUP BY job_title
        ORDER BY n DESC
        LIMIT 10;
    """,
}

def run_queries() -> None:
    with sqlite3.connect(DB_PATH) as conn:
        for title, query in QUERIES.items():
            print("\n" + "=" * 70)
            print(title)
            print("=" * 70)
            df = pd.read_sql_query(query, conn)
            print(df.to_string(index=False))

if __name__ == "__main__":
    run_queries()