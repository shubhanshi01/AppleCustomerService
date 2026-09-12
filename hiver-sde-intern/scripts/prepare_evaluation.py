"""Create human-reviewable predictions without retrieving a golden-set item itself."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import pandas as pd

from src.agent.pipeline import SupportAgent
from src.config import GOLDEN, PROCESSED
from src.retrieval.retriever import ReplyRetriever

OUT = Path(__file__).resolve().parents[1] / "data" / "evaluation" / "apple_predictions.csv"
REVIEW_COLUMNS = [
    "retrieval_top1_relevant",
    "response_grounded",
    "response_helpful_1_to_5",
    "llm_groundedness_1_to_5",
    "llm_helpfulness_1_to_5",
    "llm_safety_1_to_5",
    "llm_tone_1_to_5",
    "review_notes",
]


def main():
    golden = pd.read_csv(GOLDEN, dtype={"tweet_id": "string"})
    pairs = pd.read_csv(PROCESSED / "apple_reply_pairs.csv", dtype={"tweet_id": "string"})

    # Removing all golden tweet IDs prevents an exact historical pair from appearing as its own evidence.
    candidates = pairs[~pairs.tweet_id.isin(set(golden.tweet_id))].copy()
    agent = SupportAgent(ReplyRetriever(candidates))
    rows = []
    for row in golden.itertuples(index=False):
        result = agent.respond(row.customer_text)
        top = result["evidence"][0] if result["evidence"] else {}
        rows.append({
            "tweet_id": row.tweet_id,
            "split": row.split,
            "customer_text": row.customer_text,
            "gold_intent": row.gold_intent,
            "gold_escalate": row.gold_escalate,
            "predicted_intent": result["intent"],
            "intent_confidence": result["confidence"],
            "predicted_escalate": result["escalate"],
            "escalation_reason": result["escalation_reason"],
            "draft_reply": result["draft_reply"],
            "retrieved_customer_text": top.get("customer_text", ""),
            "retrieved_historical_reply": top.get("historical_reply", ""),
            "retrieval_score": top.get("score", 0.0),
        })
    output = pd.DataFrame(rows)

    # Keep previous human and LLM review columns when predictions are regenerated.
    if OUT.exists():
        old = pd.read_csv(OUT, dtype={"tweet_id": "string"})
        keep = [column for column in REVIEW_COLUMNS if column in old.columns]
        if keep:
            output = output.merge(old[["tweet_id", *keep]], on="tweet_id", how="left")
    for column in REVIEW_COLUMNS:
        if column not in output:
            output[column] = ""
    OUT.parent.mkdir(parents=True, exist_ok=True)
    output.to_csv(OUT, index=False)
    print(f"Wrote {len(output)} predictions to {OUT}")
    print("Review retrieval_top1_relevant, response_grounded, and response_helpful_1_to_5 before running evaluation.")


if __name__ == "__main__":
    main()
