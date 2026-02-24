📊 Job Market Data Pipeline (CSV → ETL → SQLite → SQL Analytics)

An end-to-end mini Data Engineering project built from a real-world salary dataset (salaries.csv).

This repository demonstrates graduate-level skills aligned with Data Engineer, Data Analyst, and BI Developer roles:

✅ Reproducible ETL pipeline (Python + Pandas)

✅ Data quality validation (duplicates, missing values)

✅ Business KPI computation

✅ SQLite database integration

✅ SQL analytical queries

✅ Clean repository structure & Git hygiene

🚀 Project Overview

The objective of this project is to simulate a real-world data workflow:

Ingest raw job salary data

Clean and standardize it

Compute business-ready KPIs

Load cleaned data into a relational database

Run analytical SQL queries for BI insights

This mirrors a simplified production-style data pipeline.

📂 Project Structure
job-market-data-pipeline/
├─ app/                     # (Next step: Streamlit dashboard)
│  └─ streamlit_app.py
│
├─ data/
│  ├─ raw/                  # Raw dataset (NOT tracked by git)
│  └─ processed/            # Cleaned data + SQLite DB (NOT tracked)
│
├─ notebooks/               # Optional exploration notebooks
│
├─ src/
│  ├─ etl.py                # CSV → cleaned CSV + KPI metrics
│  ├─ load.py               # Load cleaned CSV into SQLite
│  ├─ sql_metrics.py        # Analytical SQL queries
│  ├─ transform.py          # (Reserved for future transformations)
│  └─ skills_extraction.py  # (Reserved for future NLP)
│
├─ tests/                   # (Future automated tests)
├─ requirements.txt
└─ README.md
📦 Dataset

This project expects a CSV file named:

salaries.csv

Place it in:

data/raw/salaries.csv

Expected columns:

work_year,experience_level,employment_type,job_title,salary,
salary_currency,salary_in_usd,employee_residence,
remote_ratio,company_location,company_size

⚠️ The dataset is not committed to GitHub (best practice for data projects).

⚙️ Setup (WSL / Linux / macOS)
1️⃣ Clone the repository
git clone https://github.com/YOUR_USERNAME/job-market-data-pipeline.git
cd job-market-data-pipeline
2️⃣ Create a virtual environment
python3 -m venv venv
source venv/bin/activate

You should now see (venv) in your terminal.

3️⃣ Install dependencies
pip install -r requirements.txt
▶️ Run the ETL Pipeline
python src/etl.py
What the ETL does:

Loads 100k+ salary records

Removes duplicate entries

Standardizes experience levels

Validates missing values

Computes salary KPIs

Exports cleaned dataset to:

data/processed/salaries_cleaned.csv
📊 Example Output Metrics

From the current dataset:

Records processed: 105,434

Duplicates removed: 52,997 (50.3%)

Average salary (USD): 151,665

Median salary (USD): 139,475

Top roles: Data Scientist, Data Engineer, Data Analyst

Remote ratio: ~24.45% fully remote

Top locations: US, CA, GB

(Results may vary depending on dataset version.)

🗄 Load Data into SQLite

Create a local SQLite database from the cleaned dataset:

python src/load.py

This generates:

data/processed/jobs.db

Automatically created indexes:

work_year

job_title

company_location

experience_level

These improve analytical query performance.

📈 Run Analytical SQL Queries
python src/sql_metrics.py

This produces portfolio-ready analytics including:

Top 10 job titles

Salary by experience level

Remote distribution (%)

Top 10 locations

US-specific job demand

🧠 Skills Demonstrated

✔ Data ingestion and transformation
✔ Data quality validation
✔ KPI generation for BI
✔ Relational database integration
✔ SQL aggregation queries
✔ Clean project architecture
✔ Git best practices (raw data ignored)

🔜 Roadmap

Build Streamlit dashboard connected to SQLite

Add automated tests (pytest)

Add CI with GitHub Actions

Extend to skill extraction (NLP pipeline)

Deploy dashboard publicly

🛠 Technical Stack

Python

Pandas

SQLite

SQL

Streamlit (next phase)

Git & GitHub

📄 License

MIT