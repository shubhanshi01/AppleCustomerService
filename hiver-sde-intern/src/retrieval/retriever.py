from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel

class ReplyRetriever:
    def __init__(self, examples):
        self.examples = examples.reset_index(drop=True).copy()
        if self.examples.empty:
            raise ValueError("ReplyRetriever requires at least one retrieval example.")
        required = {"customer_text", "support_reply"}
        missing = required.difference(self.examples.columns)
        if missing:
            raise ValueError(
                f"Retrieval examples are missing required columns: {sorted(missing)}"
            )
        self.vectorizer = TfidfVectorizer(ngram_range=(1, 2), min_df=1, stop_words="english")
        self.matrix = self.vectorizer.fit_transform(self.examples.customer_text.fillna(""))

    def search(self, text, k=3):
        scores = linear_kernel(self.vectorizer.transform([text]), self.matrix).ravel()
        indexes = scores.argsort()[::-1][:k]
        return [{"customer_text": self.examples.iloc[i].customer_text, "historical_reply": self.examples.iloc[i].support_reply, "score": float(scores[i])} for i in indexes]
