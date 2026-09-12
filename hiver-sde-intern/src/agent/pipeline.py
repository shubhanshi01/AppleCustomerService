from src.intent.classifier import KeywordIntentClassifier
from src.agent.escalation import decide_escalation
from src.generation.generator import draft_reply

class SupportAgent:
    def __init__(self, retriever):
        self.classifier = KeywordIntentClassifier()
        self.retriever = retriever

    def respond(self, message):
        prediction = self.classifier.predict(message)
        evidence = self.retriever.search(message, k=3)
        top_score = evidence[0]["score"] if evidence else 0.0
        escalate, reason = decide_escalation(message, prediction["intent"], prediction["confidence"], top_score)
        return {**prediction, "draft_reply": draft_reply(message, prediction["intent"], evidence, escalate), "escalate": escalate, "escalation_reason": reason, "evidence": evidence}
