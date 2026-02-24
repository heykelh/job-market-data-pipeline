# 📊 Job Market Data Pipeline (CSV → Clean Dataset → Metrics)

An end-to-end mini data engineering project built from a real-world salary dataset (`salaries.csv`).
It includes a reproducible ETL pipeline (Python + Pandas) that cleans the data, removes duplicates, and outputs **CV-ready metrics** for analytics and BI.

This repository is designed to demonstrate core skills aligned with graduate data roles:
- **Data Engineering** (ETL, data quality, reproducible pipeline)
- **Data Analysis / BI** (key KPIs and insights)
- **Professional practices** (project structure, virtual environment, Git hygiene)

---

## ✅ Current Output (from ETL run)

From the latest run on the provided dataset:

- **Records processed:** 105,434
- **Duplicates removed:** 52,997 (**50.3%**)
- **Missing values:** 0 (before/after cleaning)

### Key Insights
- **Average salary (USD):** 151,665  
- **Median salary (USD):** 139,475  
- **Top roles:** Data Scientist, Data Engineer, Data Analyst  
- **Remote adoption:** ~24.45% fully remote  
- **Top locations:** US, CA, GB

> Note: Numbers may vary depending on the dataset version.

---

## 🏗 Project Structure

```text
job-market-data-pipeline/
├─ app/                    # Streamlit dashboard (coming next)
│  └─ streamlit_app.py
├─ data/
│  ├─ raw/                 # Place raw CSV here (not tracked by git)
│  └─ processed/           # Cleaned output (not tracked by git)
├─ notebooks/              # Exploration notebooks (optional)
├─ src/
│  ├─ etl.py               # CSV → cleaned CSV + metrics
│  ├─ transform.py         # (reserved)
│  ├─ load.py              # (next step: SQLite load)
│  ├─ skills_extraction.py # (reserved)
├─ tests/                  # (optional)
├─ requirements.txt
└─ README.md