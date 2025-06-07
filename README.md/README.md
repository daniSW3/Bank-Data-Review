# Bank Reviews Scraper
Scrapes Google Play Store reviews for three banks, preprocesses data, and saves it as a CSV.

## Methodology
- Scrape reviews using `google-play-scraper`.
- Collect 400+ reviews per bank (1,200 total).
- Preprocess: remove duplicates, normalize dates, handle missing data.
- Save as CSV with columns: review, rating, date, bank, source.
- Managed via GitHub with commits on `task-1` branch.

## Setup
1. Clone the repo: `git clone <repo-url>`
2. Install dependencies: `pip install -r requirements.txt`
3. Run scraper: `python scrape_reviews.py`
4. Run preprocessing: `python preprocess.py`
## Updates
- Updated bank names to Commercial Bank of Ethiopia (CBE), Bank of Abyssinia (BOA), and Dashen Bank.
- Set `country="et"` to scrape reviews from Ethiopia.
- Collected X reviews for CBE, Y for BOA, and Z for Dashen Bank.
## Task 2: Sentiment and Thematic Analysis
- Performed sentiment analysis using DistilBERT (`distilbert-base-uncased-finetuned-sst-2-english`).
- Extracted keywords using spaCy and clustered into 3–5 themes per bank (e.g., Account Access Issues, Transaction Performance).
- Saved results to `analysis_results.csv` and `sentiment_aggregation.csv`.
- Themes identified:
  - CBE: [List themes, e.g., Account Access Issues (50 reviews)]
  - BOA: [List themes]
  - Dashen Bank: [List themes]