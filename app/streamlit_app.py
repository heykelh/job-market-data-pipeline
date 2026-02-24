import os
import sqlite3
import tempfile
from pathlib import Path

import pandas as pd
import streamlit as st
import plotly.express as px

from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.pipeline import Pipeline
from sklearn.linear_model import Ridge
from sklearn.metrics import mean_absolute_error, r2_score

# ------------------------
# Paths (Cloud-safe)
# ------------------------
BASE_DIR = Path(__file__).resolve().parents[1]  # repo root
SAMPLE_CSV = BASE_DIR / "data" / "sample" / "salaries_sample.csv"

DB_PATH = Path(tempfile.gettempdir()) / "jobs.db"  # writable on Streamlit Cloud
TABLE_NAME = "jobs"

# ------------------------
# UI header
# ------------------------
st.set_page_config(page_title="Job Market Dashboard", layout="wide")
st.title("📊 Job Market Analytics Dashboard")
st.caption("ETL → SQLite → SQL Analytics → (Mini) ML Salary Predictor")


# ------------------------
# Helpers
# ------------------------
def ensure_sqlite_db() -> None:
    """Create SQLite DB from versioned sample CSV if DB doesn't exist."""
    if DB_PATH.exists():
        return

    if not SAMPLE_CSV.exists():
        st.error(f"Sample dataset not found: {SAMPLE_CSV}")
        st.info("Expected a committed file: data/sample/salaries_sample.csv")
        st.stop()

    df = pd.read_csv(SAMPLE_CSV)

    with sqlite3.connect(str(DB_PATH)) as conn:
        df.to_sql(TABLE_NAME, conn, if_exists="replace", index=False)
        conn.execute(f"CREATE INDEX IF NOT EXISTS idx_jobs_year ON {TABLE_NAME}(work_year);")
        conn.execute(f"CREATE INDEX IF NOT EXISTS idx_jobs_title ON {TABLE_NAME}(job_title);")
        conn.execute(f"CREATE INDEX IF NOT EXISTS idx_jobs_location ON {TABLE_NAME}(company_location);")
        conn.execute(f"CREATE INDEX IF NOT EXISTS idx_jobs_experience ON {TABLE_NAME}(experience_level);")
        conn.commit()


@st.cache_data
def load_data_from_sqlite() -> pd.DataFrame:
    ensure_sqlite_db()
    with sqlite3.connect(str(DB_PATH)) as conn:
        df = pd.read_sql_query(f"SELECT * FROM {TABLE_NAME}", conn)
    return df


# ------------------------
# Load data (with visible status)
# ------------------------
with st.expander("🔎 App Status (for debugging / demo reliability)", expanded=False):
    st.write("Repo root:", str(BASE_DIR))
    st.write("Sample CSV exists:", SAMPLE_CSV.exists())
    st.write("Sample CSV path:", str(SAMPLE_CSV))
    st.write("SQLite DB path (tmp):", str(DB_PATH))
    st.write("SQLite DB exists:", DB_PATH.exists())

df = load_data_from_sqlite()

if df is None or df.empty:
    st.error("Dataset loaded but is empty. Please verify the sample CSV content.")
    st.stop()

st.success(f"✅ Loaded {len(df):,} rows from SQLite")

# ------------------------
# Tabs
# ------------------------
tab_dash, tab_ml = st.tabs(["📈 Dashboard", "🤖 Salary Predictor (ML)"])


# ========================
# DASHBOARD
# ========================
with tab_dash:
    st.sidebar.header("Filters")

    years = sorted(df["work_year"].dropna().unique())
    if not years:
        st.error("No years found in dataset.")
        st.stop()

    selected_year = st.sidebar.selectbox("Year", years, index=len(years) - 1)

    exp_levels = sorted(df["experience_level"].dropna().unique())
    selected_exp = st.sidebar.multiselect("Experience Level", exp_levels, default=exp_levels)

    locations = sorted(df["company_location"].dropna().unique())
    default_locs = ["US"] if "US" in locations else locations[:1]
    selected_loc = st.sidebar.multiselect("Company Location", locations, default=default_locs)

    remote_opts = sorted(df["remote_ratio"].dropna().unique())
    selected_remote = st.sidebar.multiselect("Remote Ratio", remote_opts, default=remote_opts)

    filtered = df[
        (df["work_year"] == selected_year)
        & (df["experience_level"].isin(selected_exp))
        & (df["company_location"].isin(selected_loc))
        & (df["remote_ratio"].isin(selected_remote))
    ].copy()

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Jobs", f"{len(filtered):,}")
    c2.metric("Avg salary (USD)", f"{filtered['salary_in_usd'].mean():,.0f}" if len(filtered) else "—")
    c3.metric("Median salary (USD)", f"{filtered['salary_in_usd'].median():,.0f}" if len(filtered) else "—")
    c4.metric("Fully remote (%)", f"{(filtered['remote_ratio'].eq(100).mean()*100):.1f}%" if len(filtered) else "—")

    st.markdown("---")

    st.subheader("Salary Distribution")
    fig_salary = px.histogram(filtered, x="salary_in_usd", nbins=40)
    st.plotly_chart(fig_salary, use_container_width=True)

    st.subheader("Top Job Titles")
    top_titles = filtered["job_title"].value_counts().head(10).reset_index()
    top_titles.columns = ["job_title", "count"]
    fig_titles = px.bar(top_titles, x="count", y="job_title", orientation="h")
    st.plotly_chart(fig_titles, use_container_width=True)

    st.subheader("Average Salary by Experience Level")
    by_exp = filtered.groupby("experience_level")["salary_in_usd"].mean().reset_index()
    fig_exp = px.bar(by_exp, x="experience_level", y="salary_in_usd")
    st.plotly_chart(fig_exp, use_container_width=True)


# ========================
# ML TAB
# ========================
with tab_ml:
    st.subheader("Baseline Salary Predictor (Ridge Regression)")
    st.write(
        "A lightweight baseline model trained on the dataset to predict `salary_in_usd` "
        "from a small set of features. Intended for portfolio demonstration (training → evaluation → inference)."
    )

    feature_cols = [
        "work_year",
        "experience_level",
        "employment_type",
        "job_title",
        "remote_ratio",
        "company_location",
        "company_size",
    ]

    model_df = df.dropna(subset=feature_cols + ["salary_in_usd"]).copy()

    if len(model_df) < 200:
        st.warning("Not enough rows to train a reliable model. Increase sample size.")
        st.stop()

    X = model_df[feature_cols]
    y = model_df["salary_in_usd"]

    categorical = ["experience_level", "employment_type", "job_title", "company_location", "company_size"]
    numeric = ["work_year", "remote_ratio"]

    preprocessor = ColumnTransformer(
        transformers=[
            ("cat", OneHotEncoder(handle_unknown="ignore"), categorical),
            ("num", "passthrough", numeric),
        ]
    )

    pipe = Pipeline(steps=[("prep", preprocessor), ("model", Ridge(alpha=1.0))])

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    @st.cache_resource
    def train_model():
        pipe.fit(X_train, y_train)
        preds = pipe.predict(X_test)
        mae = mean_absolute_error(y_test, preds)
        r2 = r2_score(y_test, preds)
        return pipe, mae, r2

    trained_pipe, mae, r2 = train_model()

    m1, m2 = st.columns(2)
    m1.metric("MAE (USD)", f"{mae:,.0f}")
    m2.metric("R²", f"{r2:.3f}")

    st.markdown("### Try a prediction")

    colA, colB, colC = st.columns(3)

    with colA:
        year_in = st.selectbox("Work year", sorted(model_df["work_year"].unique()))
        exp_in = st.selectbox("Experience level", sorted(model_df["experience_level"].unique()))
        emp_in = st.selectbox("Employment type", sorted(model_df["employment_type"].unique()))

    with colB:
        # limit to avoid huge dropdown
        titles = sorted(model_df["job_title"].unique())
        title_in = st.selectbox("Job title", titles[:200])
        remote_in = st.selectbox("Remote ratio", sorted(model_df["remote_ratio"].unique()))

    with colC:
        loc_in = st.selectbox("Company location", sorted(model_df["company_location"].unique()))
        size_in = st.selectbox("Company size", sorted(model_df["company_size"].unique()))

    if st.button("Predict salary (USD)"):
        input_df = pd.DataFrame([{
            "work_year": year_in,
            "experience_level": exp_in,
            "employment_type": emp_in,
            "job_title": title_in,
            "remote_ratio": remote_in,
            "company_location": loc_in,
            "company_size": size_in,
        }])

        pred = trained_pipe.predict(input_df)[0]
        st.success(f"Predicted salary (USD): {pred:,.0f}")
        st.caption("Note: Baseline model for demonstration purposes (not production).")