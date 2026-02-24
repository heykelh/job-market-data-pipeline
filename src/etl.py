import os
import pandas as pd

RAW_PATH = "data/raw/salaries.csv"
PROCESSED_PATH = "data/processed/salaries_cleaned.csv"


def load_data(path: str) -> pd.DataFrame:
    print("Loading dataset...")
    df = pd.read_csv(path)
    print(f"Dataset loaded with {df.shape[0]} rows and {df.shape[1]} columns")
    return df


def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    print("\nCleaning dataset...")

    initial_rows = df.shape[0]

    # Remove duplicates
    df = df.drop_duplicates().copy()
    after_dedup = df.shape[0]

    # Standardize experience levels
    exp_map = {"EN": "Entry", "MI": "Mid", "SE": "Senior", "EX": "Executive"}
    df.loc[:, "experience_level"] = df["experience_level"].map(exp_map)

    # Basic sanity checks
    missing_before = int(df.isna().sum().sum())
    df = df.dropna().copy()
    missing_after = int(df.isna().sum().sum())

    # --- Data Quality Metrics ---
    print("\nData Quality Metrics:")
    print(f"Duplicates removed: {initial_rows - after_dedup} ({((initial_rows - after_dedup)/initial_rows)*100:.1f}%)")
    print(f"Missing values before cleaning: {missing_before}")
    print(f"Missing values after cleaning: {missing_after}")

    # --- Business Insights (CV-ready) ---
    print("\nBusiness Insights:")

    avg_salary = df["salary_in_usd"].mean()
    median_salary = df["salary_in_usd"].median()
    print(f"Average salary (USD): {avg_salary:,.0f}")
    print(f"Median salary (USD): {median_salary:,.0f}")

    print("\nTop 5 job titles:")
    print(df["job_title"].value_counts().head(5).to_string())

    print("\nRemote ratio distribution (%):")
    remote_pct = (df["remote_ratio"].value_counts(normalize=True) * 100).round(2)
    print(remote_pct.sort_index().to_string())

    print("\nTop 5 company locations:")
    print(df["company_location"].value_counts().head(5).to_string())

    return df


def save_data(df: pd.DataFrame, path: str) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    df.to_csv(path, index=False)
    print(f"\nCleaned dataset saved to {path}")


def main():
    df = load_data(RAW_PATH)
    df_cleaned = clean_data(df)
    save_data(df_cleaned, PROCESSED_PATH)


if __name__ == "__main__":
    main()