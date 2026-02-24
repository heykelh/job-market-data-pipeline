import os
import sqlite3
import pandas as pd
import streamlit as st
import plotly.express as px

from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.pipeline import Pipeline
from sklearn.linear_model import Ridge
from sklearn.metrics import mean_absolute_error, r2_score

DB_PATH = "data/processed/jobs.db"
TABLE_NAME = "jobs"
SAMPLE_CSV = "data/sample/salaries_sample.csv"

st.set_page_config(page_title="Job Market Dashboard", layout="wide")
st.title("📊 Job Market Analytics Dashboard")
st.caption("ETL → SQLite → SQL Analytics → (Mini) ML Salary Predictor")


# ------------------------
# Helpers: ensure DB exists (for Streamlit Cloud / portable demo)
# ------------------------
def ensure_sqlite_db():
    """
    If local SQLite DB doesn't exist (e.g., Streamlit Cloud),
    create it from the versioned sample CSV included in the repo.
    """
    if os.path.exists(DB_PATH):
        return

    if not os.path.exists(SAMPLE_CSV):
        raise FileNotFoundError(
            f"Database not found at: {DB_PATH}\n"
            f"Sample CSV not found at: {SAMPLE_CSV}\n\n"
            "Fix:\n"
            "- Generate sample: python src/make_sample.py\n"
            "- Or run full pipeline locally: python src/etl.py && python src/load.py"
        )

    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    df = pd.read_csv(SAMPLE_CSV)

    with sqlite3.connect(DB_PATH) as conn:
        df.to_sql(TABLE_NAME, conn, if_exists="replace", index=False)

        # Indexes for faster filtering/aggregations
        conn.execute(f"CREATE INDEX IF NOT EXISTS idx_jobs_year ON {TABLE_NAME}(work_year);")
        conn.execute(f"CREATE INDEX IF NOT EXISTS idx_jobs_title ON {TABLE_NAME}(job_title);")
        conn.execute(f"CREATE INDEX IF NOT EXISTS idx_jobs_location ON {TABLE_NAME}(company_location);")
        conn.execute(f"CREATE INDEX IF NOT EXISTS idx_jobs_experience ON {TABLE_NAME}(experience_level);")
        conn.commit()


@st.cache_data
def load_data_from_sqlite() -> pd.DataFrame:
    ensure_sqlite_db()
    with sqlite3.connect(DB_PATH) as conn:
        df = pd.read_sql_query(f"SELECT * FROM {TABLE_NAME}", conn)
    return df


df = load_data_from_sqlite()