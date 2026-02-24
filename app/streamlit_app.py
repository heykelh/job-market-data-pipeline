import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px

DB_PATH = "data/processed/jobs.db"

st.set_page_config(page_title="Job Market Dashboard", layout="wide")

st.title("📊 Job Market Analytics Dashboard")
st.markdown("Data Engineering Portfolio Project")

# ------------------------
# Load data
# ------------------------
@st.cache_data
def load_data():
    with sqlite3.connect(DB_PATH) as conn:
        df = pd.read_sql_query("SELECT * FROM jobs", conn)
    return df


df = load_data()

# ------------------------
# Sidebar Filters
# ------------------------
st.sidebar.header("Filters")

years = sorted(df["work_year"].unique())
selected_year = st.sidebar.selectbox("Select Year", years)

experience_levels = df["experience_level"].unique()
selected_experience = st.sidebar.multiselect(
    "Experience Level", experience_levels, default=experience_levels
)

locations = df["company_location"].unique()
selected_location = st.sidebar.multiselect(
    "Company Location", locations, default=["US"]
)

remote_options = df["remote_ratio"].unique()
selected_remote = st.sidebar.multiselect(
    "Remote Ratio", remote_options, default=remote_options
)

# Apply filters
filtered_df = df[
    (df["work_year"] == selected_year) &
    (df["experience_level"].isin(selected_experience)) &
    (df["company_location"].isin(selected_location)) &
    (df["remote_ratio"].isin(selected_remote))
]

# ------------------------
# KPI Section
# ------------------------
col1, col2, col3 = st.columns(3)

col1.metric("Total Jobs", f"{len(filtered_df):,}")
col2.metric("Average Salary (USD)", f"{filtered_df['salary_in_usd'].mean():,.0f}")
col3.metric("Median Salary (USD)", f"{filtered_df['salary_in_usd'].median():,.0f}")

st.markdown("---")

# ------------------------
# Salary Distribution
# ------------------------
st.subheader("Salary Distribution")

fig_salary = px.histogram(
    filtered_df,
    x="salary_in_usd",
    nbins=50,
    title="Salary Distribution",
)

st.plotly_chart(fig_salary, use_container_width=True)

# ------------------------
# Top Job Titles
# ------------------------
st.subheader("Top Job Titles")

top_titles = (
    filtered_df["job_title"]
    .value_counts()
    .head(10)
    .reset_index()
)

top_titles.columns = ["job_title", "count"]

fig_titles = px.bar(
    top_titles,
    x="count",
    y="job_title",
    orientation="h",
    title="Top 10 Job Titles"
)

st.plotly_chart(fig_titles, use_container_width=True)

# ------------------------
# Salary by Experience
# ------------------------
st.subheader("Average Salary by Experience Level")

salary_by_exp = (
    filtered_df
    .groupby("experience_level")["salary_in_usd"]
    .mean()
    .reset_index()
)

fig_exp = px.bar(
    salary_by_exp,
    x="experience_level",
    y="salary_in_usd",
    title="Average Salary by Experience Level"
)

st.plotly_chart(fig_exp, use_container_width=True)