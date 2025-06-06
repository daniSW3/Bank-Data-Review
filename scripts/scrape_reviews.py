from google_play_scraper import app, reviews
import pandas as pd
from datetime import datetime
import os

# Define bank apps
banks = [
    {"name": " Commercial Bank of Ethiopia", "app_id": "com.cbe.cbe"},
    {"name": "Bank of Abyssinia (BOA)", "app_id": "com.boa.mobile"},
    {"name": "Dashen Bank", "app_id": "com.dashenmobilebankinge"}
]

# Function to scrape reviews
def scrape_bank_reviews(bank, num_reviews=400):
    result, _ = reviews(
        bank["app_id"],
        lang="en",  # English reviews
        country="us",  # US reviews
        count=num_reviews,  # Number of reviews
        sort="newest"  # Sort by newest
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
    all_reviews.extend(reviews_data)

# Save to CSV
df = pd.DataFrame(all_reviews)
output_file = "raw_reviews.csv"
df.to_csv(output_file, index=False, encoding="utf-8")
print(f"Saved {len(df)} reviews to {output_file}")

# Commit to Git
if __name__ == "__main__":
    os.system('git add scrape_reviews.py raw_reviews.csv')
    os.system('git commit -m "Add scraping script and raw reviews data"')
    os.system('git push origin task-1')