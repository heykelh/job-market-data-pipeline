import os
import sqlite3
import pandas as pd

CLEAN_PATH = "data/processed/salaries_cleaned.csv"
DB_PATH = "data/processed/jobs.db"
TABLE_NAME = "jobs"


def load_clean_csv(path: str) -> pd.DataFrame:
    if not os.path.exists(path):
        raise FileNotFoundError(
            f"Clean file not found: {path}\n"
            "Run: python src/etl.py (and ensure salaries.csv is in data/raw/)"
        )
    return pd.read_csv(path)


def create_db_and_load(df: pd.DataFrame, db_path: str, table_name: str) -> None:
    os.makedirs(os.path.dirname(db_path), exist_ok=True)

    with sqlite3.connect(db_path) as conn:
        df.to_sql(table_name, conn, if_exists="replace", index=False)

        # Useful indexes for analytics / BI queries
        conn.execute(f"CREATE INDEX IF NOT EXISTS idx_jobs_year ON {table_name}(work_year);")
        conn.execute(f"CREATE INDEX IF NOT EXISTS idx_jobs_title ON {table_name}(job_title);")
        conn.execute(f"CREATE INDEX IF NOT EXISTS idx_jobs_location ON {table_name}(company_location);")
        conn.execute(f"CREATE INDEX IF NOT EXISTS idx_jobs_experience ON {table_name}(experience_level);")
        conn.commit()


def main():
    print("Loading cleaned CSV...")
    df = load_clean_csv(CLEAN_PATH)
    print(f"Loaded {len(df):,} rows")

    print("Creating SQLite database and loading table...")
    create_db_and_load(df, DB_PATH, TABLE_NAME)

    print(f"✅ SQLite DB created: {DB_PATH}")
    print(f"✅ Table loaded: {TABLE_NAME}")


if __name__ == "__main__":
    main()