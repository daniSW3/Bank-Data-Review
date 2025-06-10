import pandas as pd
import spacy
from transformers import pipeline
from collections import defaultdict
import os

# Load spaCy model
nlp = spacy.load("en_core_web_sm")

# Load DistilBERT sentiment analysis pipeline
sentiment_analyzer = pipeline("sentiment-analysis", model="distilbert-base-uncased-finetuned-sst-2-english")

# Load reviews
df = pd.read_csv("raw_reviews.csv")
df["review_id"] = df.index  # Add review_id column

# Preprocessing function
def preprocess_text(text):
    doc = nlp(text.lower())
    tokens = [token.lemma_ for token in doc if not token.is_stop and not token.is_punct and token.is_alpha]
    return tokens

# Sentiment analysis function
def get_sentiment(review):
    try:
        result = sentiment_analyzer(review)[0]
        label = result["label"].lower()  # POSITIVE or NEGATIVE
        score = result["score"]
        return label, score
    except Exception as e:
        print(f"Error processing review: {e}")
        return "neutral", 0.0  # Fallback for long reviews

# Keyword extraction function
def extract_keywords(text):
    doc = nlp(text)
    keywords = [chunk.text.lower() for chunk in doc.noun_chunks if len(chunk.text.split()) <= 3]
    return keywords

# Theme clustering function
def assign_themes(keywords, bank):
    themes = {
        "Account Access Issues": ["login", "authentication", "password", "access", "sign in"],
        "Transaction Performance": ["transfer", "payment", "slow", "failed", "transaction"],
        "User Interface & Experience": ["ui", "interface", "crash", "app design", "user experience"],
        "Customer Support": ["support", "service", "help", "response", "customer"],
        "Feature Requests": ["feature", "update", "fingerprint", "option", "request"]
    }
    assigned_themes = []
    for theme, theme_keywords in themes.items():
        if any(any(kw in keyword for kw in theme_keywords) for keyword in keywords):
            assigned_themes.append(theme)
    return assigned_themes if assigned_themes else ["Other"]

# Process reviews
print("Processing reviews...")
df["tokens"] = df["review"].apply(preprocess_text)
df["keywords"] = df["review"].apply(extract_keywords)
df[["sentiment_label", "sentiment_score"]] = df["review"].apply(lambda x: pd.Series(get_sentiment(x)))
df["themes"] = df.apply(lambda row: assign_themes(row["keywords"], row["bank"]), axis=1)

# Aggregate sentiment by bank and rating
sentiment_agg = df.groupby(["bank", "rating"]).agg({
    "sentiment_score": "mean",
    "review_id": "count"
}).rename(columns={"review_id": "count"}).reset_index()
print("Sentiment aggregation:\n", sentiment_agg)

# Aggregate themes by bank
theme_counts = defaultdict(lambda: defaultdict(int))
for _, row in df.iterrows():
    bank = row["bank"]
    for theme in row["themes"]:
        theme_counts[bank][theme] += 1

print("\nThemes per bank:")
for bank, themes in theme_counts.items():
    print(f"\n{bank}:")
    for theme, count in themes.items():
        print(f"  {theme}: {count} reviews")

# Save results
output_file = "analysis_results.csv"
df[["review_id", "review", "sentiment_label", "sentiment_score", "themes", "bank"]].to_csv(output_file, index=False, encoding="utf-8")
print(f"Saved analysis results to {output_file}")

# Save aggregated sentiment
sentiment_agg.to_csv("sentiment_aggregation.csv", index=False, encoding="utf-8")
print("Saved sentiment aggregation to sentiment_aggregation.csv")

# Commit to Git
if __name__ == "__main__":
    os.system('git add analyze_reviews.py analysis_results.csv sentiment_aggregation.csv')
    os.system('git commit -m "Add sentiment and thematic analysis for task-2"')
    os.system('git push origin task-2')