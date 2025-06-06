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