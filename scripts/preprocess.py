import pandas as pd
from datetime import datetime

# Load raw data
df = pd.read_csv("raw_reviews.csv")

# 1. Remove duplicates
print(f"Initial rows: {len(df)}")
df = df.drop_duplicates(subset=["review", "date", "bank"], keep="first")
print(f"Rows after removing duplicates: {len(df)}")

# 2. Handle missing data
# Drop rows where 'review' or 'rating' is missing
df = df.dropna(subset=["review", "rating"])
print(f"Rows after dropping missing reviews/ratings: {len(df)}")
# Fill missing 'date' with a placeholder (or impute if needed)
df["date"] = df["date"].fillna("1970-01-01")

# 3. Normalize dates (ensure YYYY-MM-DD)
def normalize_date(date_str):
    try:
        return pd.to_datetime(date_str).strftime("%Y-%m-%d")
    except:
        return "1970-01-01"  # Fallback for invalid dates
df["date"] = df["date"].apply(normalize_date)

# 4. Ensure rating is an integer (1-5)
df["rating"] = df["rating"].astype(int)
df = df[df["rating"].between(1, 5)]

# 5. Save clean dataset
clean_file = "clean_reviews.csv"
df.to_csv(clean_file, index=False, encoding="utf-8")
print(f"Saved clean dataset to {clean_file}")

# 6. Verify KPIs
print(f"Total reviews: {len(df)}")
print(f"Missing data:\n{df.isna().sum()}")
print(f"Columns: {list(df.columns)}")

# Commit to Git
import os
os.system('git add preprocess.py clean_reviews.csv')
os.system('git commit -m "Add preprocessing script and clean dataset"')
os.system('git push origin task-1')