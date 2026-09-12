import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import json
import pandas as pd
from sklearn.metrics import accuracy_score, f1_score, precision_recall_fscore_support
from src.config import GOLDEN

PREDICTIONS = Path(__file__).resolve().parents[1] / "data" / "evaluation" / "apple_predictions.csv"


def measured_or_pending(data, truth, prediction, metric):
    usable = data.dropna(subset=[truth, prediction])
    usable = usable[(usable[truth].astype(str).str.strip() != "") & (usable[prediction].astype(str).str.strip() != "")]
    if usable.empty:
        return "Not measured yet"
    return metric(usable)

def main():
    if not PREDICTIONS.exists():
        raise SystemExit("Prediction file is missing. Run: python scripts/prepare_evaluation.py")
    predictions = pd.read_csv(PREDICTIONS, dtype={"tweet_id": "string"})
    reviewed = predictions.merge(pd.read_csv(GOLDEN, dtype={"tweet_id": "string"})[["tweet_id", "reviewed"]], on="tweet_id", how="left")
    reviewed = reviewed[reviewed.reviewed.astype(str).str.lower().eq("true")].copy()
    report = {"n_reviewed": int(len(reviewed))}
    report["intent_accuracy"] = measured_or_pending(reviewed, "gold_intent", "predicted_intent", lambda x: accuracy_score(x.gold_intent, x.predicted_intent))
    report["intent_macro_f1"] = measured_or_pending(reviewed, "gold_intent", "predicted_intent", lambda x: f1_score(x.gold_intent, x.predicted_intent, average="macro"))
    report["escalation_accuracy"] = measured_or_pending(reviewed, "gold_escalate", "predicted_escalate", lambda x: accuracy_score(x.gold_escalate.astype(str).str.lower(), x.predicted_escalate.astype(str).str.lower()))
    report["retrieval_top1_relevance"] = measured_or_pending(reviewed, "retrieval_top1_relevant", "retrieval_score", lambda x: float(x.retrieval_top1_relevant.astype(str).str.lower().eq("true").mean()))
    report["response_grounding_rate"] = measured_or_pending(reviewed, "response_grounded", "draft_reply", lambda x: float(x.response_grounded.astype(str).str.lower().eq("true").mean()))
    report["response_helpfulness_mean"] = measured_or_pending(reviewed, "response_helpful_1_to_5", "draft_reply", lambda x: float(pd.to_numeric(x.response_helpful_1_to_5).mean()))
    print(json.dumps(report, indent=2))

if __name__ == "__main__": main()
