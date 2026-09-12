from collections import Counter
from src.config import INTENTS
from src.intent.taxonomy import KEYWORDS

class KeywordIntentClassifier:
    """Transparent operational baseline used to bootstrap labels and route low-confidence cases."""
    def predict(self, text):
        value = (text or "").lower()
        scores = {intent: sum(term in value for term in terms) for intent, terms in KEYWORDS.items()}
        best = max(scores, key=scores.get)
        total = sum(scores.values())
        return {"intent": best if scores[best] else "other", "confidence": scores[best] / total if total else 0.0, "scores": scores}

def label_from_keywords(text):
    return KeywordIntentClassifier().predict(text)["intent"]
