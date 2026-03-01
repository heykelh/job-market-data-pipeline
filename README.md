# 📊 Job Market Analytics Dashboard + 🤖 ML Salary Predictor

End-to-end Data Engineering + Analytics + baseline Machine Learning project built from a real-world salary dataset and deployed as an interactive Streamlit application.

**Live Demo:** https://job-market-data-pipeline-heykelh.streamlit.app/#job-market-analytics-dashboard

---

## 🚀 Project Overview

This project simulates a realistic applied data workflow:

Raw CSV → Data Cleaning → Business Metrics → SQLite Database → Interactive Dashboard → Machine Learning Model → Cloud Deployment

It demonstrates practical skills aligned with:

- Data Engineering
- Business Intelligence / Analytics
- Machine Learning
- Cloud Deployment

---

## 📌 Data Source

Primary dataset:

Data Science Salaries 2025 (Kaggle)  
https://www.kaggle.com/datasets/arnabchaki/data-science-salaries-2025?resource=download&select=salaries.csv

Dataset file used: `salaries.csv`

Main columns:

- work_year  
- experience_level  
- employment_type  
- job_title  
- salary  
- salary_currency  
- salary_in_usd  
- employee_residence  
- remote_ratio  
- company_location  
- company_size  

---

## 🧪 Why a Versioned Sample Dataset Is Used

The original Kaggle dataset contains over 100,000 rows.

For deployment reliability and fast startup on Streamlit Cloud, this repository includes a curated sample:

`data/sample/salaries_sample.csv`

Why this is good engineering practice:

- Ensures reproducibility  
- Removes dependency on external downloads  
- Prevents network failures during demo  
- Improves cloud startup performance  
- Keeps repository lightweight  
- Guarantees reliable interview demonstration  

In a production system, the full dataset would be stored in cloud storage (S3, GCS, Azure Blob) or a data warehouse and ingested automatically.

---

## 🗂 Repository Structure

```
job-market-data-pipeline/
├─ app/
│  └─ streamlit_app.py
├─ data/
│  └─ sample/
│     └─ salaries_sample.csv
├─ src/
│  ├─ etl.py
│  ├─ load.py
│  ├─ sql_metrics.py
│  └─ make_sample.py
├─ requirements.txt
└─ README.md
```

---

## ⚙️ Local Setup (Linux / WSL / macOS)

### 1. Create virtual environment

```bash
python3 -m venv venv
source venv/bin/activate
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

---

## ▶️ Running the Project

### ETL (Full Dataset - Local Only)

Place Kaggle file in:

```
data/raw/salaries.csv
```

Then run:

```bash
python src/etl.py
```

Outputs:

- Cleaned dataset  
- Duplicate removal metrics  
- Salary distribution metrics  
- Remote work adoption metrics  

---

### Load into SQLite (Local Only)

```bash
python src/load.py
```

Creates:

```
data/processed/jobs.db
```

Indexes created:

- work_year  
- job_title  
- company_location  
- experience_level  

---

### Run SQL KPI Queries

```bash
python src/sql_metrics.py
```

Examples:

- Top job titles  
- Salary by experience  
- Remote distribution  
- Top hiring countries  

---

### Run Streamlit App

```bash
streamlit run app/streamlit_app.py
```

The deployed cloud version automatically uses the versioned sample dataset.

---

## 📊 Dashboard Features

- Interactive filters (year, experience, location, remote ratio)
- KPI cards (job count, avg salary, median salary, remote %)
- Salary distribution histogram
- Top job titles
- Salary by experience visualization
- Live ML prediction tab

---

## 🤖 Machine Learning Model

A baseline Ridge Regression model predicts `salary_in_usd`.

### Features Used

- work_year  
- experience_level  
- employment_type  
- job_title  
- remote_ratio  
- company_location  
- company_size  

Categorical variables are encoded using OneHotEncoder.

Pipeline:

Preprocessing → Ridge Regression

---

## 📈 ML Evaluation Metrics Explained

### MAE (Mean Absolute Error)

Average absolute difference between predicted and actual salary.

Example:

MAE = 18,000 USD  
→ Predictions are off by $18k on average.

Lower MAE indicates better performance.

---

### R² (Coefficient of Determination)

Measures how much of salary variance is explained by the model.

- 1.0 → Perfect prediction  
- 0.0 → Equivalent to predicting mean  
- Negative → Worse than baseline  

Example:

R² = 0.62  
→ 62% of salary variability is explained by selected features.

Note: This is a baseline model designed to demonstrate workflow, not a production-grade predictor.

---

## ✅ What This Project Demonstrates

Data Engineering:

- Structured ETL pipeline  
- Data quality validation  
- Clean data layering  
- SQLite indexing  

Analytics:

- KPI extraction  
- Interactive BI dashboard  

Machine Learning:

- Feature encoding  
- Model training & evaluation  
- Live inference  

Deployment:

- Streamlit Cloud hosting  
- Portable data architecture  
- Reproducible environment  

---

## 🔭 Potential Improvements

Data Quality:

- Outlier detection  
- Inflation-adjusted salary comparisons  
- Better deduplication logic  
- Missing value imputation  

Feature Engineering:

- Job title normalization  
- Regional economic indicators  
- Skill extraction via NLP  

Modeling:

- Gradient boosting models  
- Cross-validation  
- Hyperparameter tuning  
- Feature importance visualization  
- SHAP explainability  

Architecture:

- PostgreSQL instead of SQLite  
- dbt transformations  
- Airflow orchestration  
- CI/CD pipelines  
- REST API for inference  

---

## 🧾 Tech Stack

- Python  
- Pandas  
- SQLite  
- Streamlit  
- Plotly  
- Scikit-learn  
- Git & GitHub  

---

## 🎯 Conclusion

This project demonstrates a complete applied data lifecycle:

Raw data → Cleaned dataset → Database → Analytics → Machine Learning → Cloud deployment

It showcases structured engineering thinking, analytical reasoning, and deployable ML capability suitable for graduate-level data roles.

---
