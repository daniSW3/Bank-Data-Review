from google_play_scraper import app, reviews, Sort
import pandas as pd
from datetime import datetime
import os

# Define bank apps with corrected names and app IDs
banks = [
    {"name": "Commercial Bank of Ethiopia (CBE)", "app_id": "com.combanketh.mobilebanking"},
    {"name": "Bank of Abyssinia (BOA)", "app_id": "com.boa.boaMobileBanking"},
    {"name": "Dashen Bank", "app_id": "com.dashen.dashensuperapp"}
]

# Function to scrape reviews
def scrape_bank_reviews(bank, num_reviews=1000):  # Increased to ensure 400+ reviews
    result, _ = reviews(
        bank["app_id"],
        lang="en",  # English reviews
        country="et",  # Ethiopia reviews
        count=num_reviews,
        sort=Sort.NEWEST
    )
    # Extract relevant fields
    reviews_data = [
        {
            "review": review["content"],
            "rating": review["score"],
            "date": review["at"].strftime("%Y-%m-%d"),
            "bank": bank["name"],
            "source": "Google Play"
        }
        for review in result
    ]
    return reviews_data

# Scrape reviews for all banks
all_reviews = []
for bank in banks:
    print(f"Scraping reviews for {bank['name']}...")
    reviews_data = scrape_bank_reviews(bank)
    print(f"Collected {len(reviews_data)} reviews for {bank['name']}")
    all_reviews.extend(reviews_data)

# Save to CSV
df = pd.DataFrame(all_reviews)
output_file = "raw_reviews.csv"
df.to_csv(output_file, index=False, encoding="utf-8")
print(f"Saved {len(df)} reviews to {output_file}")

# Verify data quality
print(f"Total reviews: {len(df)}")
print(f"Reviews per bank:\n{df['bank'].value_counts()}")
print(f"Missing data:\n{df.isna().sum()}")

# Commit to Git
if __name__ == "__main__":
    os.system('git add scrape_reviews.py raw_reviews.csv')
    os.system('git commit -m "Update bank names and app IDs in scrape_reviews.py"')
    os.system('git push origin task-1')