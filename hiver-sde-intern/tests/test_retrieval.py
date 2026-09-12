import pandas as pd
from src.retrieval.retriever import ReplyRetriever

def test_retriever_prefers_related_case():
    data = pd.DataFrame({"customer_text": ["my battery drains quickly", "where is my order"], "support_reply": ["Battery help", "Order help"]})
    assert ReplyRetriever(data).search("battery drains", 1)[0]["historical_reply"] == "Battery help"
