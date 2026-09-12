from src.intent.classifier import KeywordIntentClassifier

def test_keyword_intent_classifier_routes_billing():
    result = KeywordIntentClassifier().predict("I was charged twice for my subscription")
    assert result["intent"] == "billing_and_purchase"
    assert result["confidence"] > 0
