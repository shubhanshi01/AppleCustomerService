"""Create customer -> immediate AppleSupport-reply pairs from the raw Kaggle CSV."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import pandas as pd
from src.config import RAW_TWEETS, PROCESSED, BRAND
from src.intent.classifier import label_from_keywords

OUT = PROCESSED / "apple_reply_pairs.csv"

def main(limit=None):
    if not RAW_TWEETS.exists():
        raise FileNotFoundError(f"Missing {RAW_TWEETS}. Run scripts/download_data.py first.")
    chunks = []
    columns = ["tweet_id", "author_id", "inbound", "text", "in_response_to_tweet_id"]
    for chunk in pd.read_csv(RAW_TWEETS, usecols=columns, chunksize=100_000):
        chunks.append(chunk)
        if limit and sum(map(len, chunks)) >= limit:
            break
    tweets = pd.concat(chunks, ignore_index=True)
    tweets["tweet_id"] = tweets.tweet_id.astype(str)
    tweets["parent"] = tweets.in_response_to_tweet_id.astype("Int64").astype(str)
    support = tweets[(tweets.author_id == BRAND) & (~tweets.inbound)].copy()
    customers = tweets[tweets.inbound].copy()
    pairs = customers.merge(support[["parent", "text"]], left_on="tweet_id", right_on="parent", how="inner", suffixes=("_customer", "_support"))
    pairs = pairs.rename(columns={"text_customer": "customer_text", "text_support": "support_reply"})
    pairs = pairs[["tweet_id", "customer_text", "support_reply"]].dropna()
    pairs = pairs[(pairs.customer_text.str.len() >= 8) & (pairs.support_reply.str.len() >= 12)].drop_duplicates("tweet_id")
    pairs["weak_intent"] = pairs.customer_text.map(label_from_keywords)
    PROCESSED.mkdir(parents=True, exist_ok=True)
    pairs.to_csv(OUT, index=False)
    print(f"Wrote {len(pairs):,} immediate customer-to-AppleSupport pairs to {OUT}")

if __name__ == "__main__": main()
