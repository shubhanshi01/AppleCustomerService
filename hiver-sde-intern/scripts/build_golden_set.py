"""Stratified annotation worksheet. Labels must be reviewed before evaluation."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import pandas as pd
from src.config import PROCESSED, GOLDEN, INTENTS

def main(n=180):
    source = pd.read_csv(PROCESSED / "apple_reply_pairs.csv")
    groups = [g.sample(min(len(g), max(1, n // len(INTENTS))), random_state=17) for _, g in source.groupby("weak_intent")]
    selected = pd.concat(groups)
    remaining = source.drop(selected.index).sample(max(0, n - len(selected)), random_state=23)
    selected = pd.concat([selected, remaining]).sample(frac=1, random_state=31).head(n).copy()
    selected["gold_intent"] = ""
    selected["gold_escalate"] = ""
    selected["gold_escalation_reason"] = ""
    selected["human_reply_score_1_to_5"] = ""
    selected["retrieval_top1_relevant"] = ""
    selected["response_grounded"] = ""
    selected["response_helpful_1_to_5"] = ""
    selected["annotation_notes"] = ""
    selected["reviewed"] = False
    selected["split"] = ["test" if i % 5 else "dev" for i in range(len(selected))]
    GOLDEN.parent.mkdir(parents=True, exist_ok=True)
    selected.to_csv(GOLDEN, index=False)
    print(f"Wrote {len(selected)}-row annotation worksheet to {GOLDEN}")

if __name__ == "__main__": main()
