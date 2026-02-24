import os
import pandas as pd

CLEAN_PATH = "data/processed/salaries_cleaned.csv"
SAMPLE_PATH = "data/sample/salaries_sample.csv"
N = 5000  # sample size (reliable + light)

def main():
    if not os.path.exists(CLEAN_PATH):
        raise FileNotFoundError(
            f"{CLEAN_PATH} not found.\n"
            "Run first: python src/etl.py"
        )

    df = pd.read_csv(CLEAN_PATH)

    sample = df.sample(n=min(N, len(df)), random_state=42).copy()
    os.makedirs(os.path.dirname(SAMPLE_PATH), exist_ok=True)
    sample.to_csv(SAMPLE_PATH, index=False)

    print(f"✅ Sample created: {SAMPLE_PATH} ({len(sample):,} rows)")

if __name__ == "__main__":
    main()