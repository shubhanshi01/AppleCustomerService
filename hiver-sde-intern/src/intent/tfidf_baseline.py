from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

class TfidfIntentClassifier:
    def __init__(self):
        self.vectorizer = TfidfVectorizer(ngram_range=(1, 2), min_df=2, sublinear_tf=True, max_features=25000)
        self.model = LogisticRegression(max_iter=1000, class_weight="balanced", random_state=7)

    def fit(self, texts, labels):
        self.model.fit(self.vectorizer.fit_transform(texts), labels)
        return self

    def predict(self, texts):
        matrix = self.vectorizer.transform(texts)
        labels = self.model.predict(matrix)
        confidence = self.model.predict_proba(matrix).max(axis=1)
        return list(zip(labels, confidence))
