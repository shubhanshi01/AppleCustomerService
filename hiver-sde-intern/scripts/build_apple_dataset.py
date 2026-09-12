from pathlib import Path
import pandas as pd
from collections import Counter

PROJECT_ROOT = Path(__file__).resolve().parents[1]
RAW_FILE = PROJECT_ROOT / "data" / "raw" / "twcs.csv"

CHUNK_SIZE = 100_000


def inspect_authors():
    print("=" * 70)
    print("STEP 3A - FINDING APPLE SUPPORT ACCOUNT")
    print("=" * 70)

    author_counts = Counter()
    outbound_counts = Counter()
    inbound_counts = Counter()

    total_rows = 0

    for chunk in pd.read_csv(
        RAW_FILE,
        chunksize=CHUNK_SIZE,
        dtype={
            "tweet_id": "int64",
            "author_id": "string",
            "inbound": "boolean",
            "created_at": "string",
            "text": "string",
            "response_tweet_id": "string",
            "in_response_to_tweet_id": "string",
        }
    ):
        total_rows += len(chunk)

        author_counts.update(
            chunk["author_id"].dropna().tolist()
        )

        outbound_counts.update(
            chunk.loc[
                chunk["inbound"] == False,
                "author_id"
            ].dropna().tolist()
        )

        inbound_counts.update(
            chunk.loc[
                chunk["inbound"] == True,
                "author_id"
            ].dropna().tolist()
        )

    print(f"\nTotal rows processed: {total_rows:,}")

    print("\nTop authors overall:")
    for author, count in author_counts.most_common(30):
        print(f"{author:30} {count:,}")

    print("\nTop outbound authors:")
    for author, count in outbound_counts.most_common(30):
        print(f"{author:30} {count:,}")

    print("\nPotential Apple-related authors:")

    apple_candidates = [
        author
        for author in author_counts
        if "apple" in str(author).lower()
    ]

    for author in sorted(
        apple_candidates,
        key=lambda x: author_counts[x],
        reverse=True
    ):
        print(
            f"{author:30} "
            f"total={author_counts[author]:,} "
            f"outbound={outbound_counts[author]:,} "
            f"inbound={inbound_counts[author]:,}"
        )


if __name__ == "__main__":
    inspect_authors()