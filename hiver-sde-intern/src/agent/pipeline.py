from src.intent.classifier import KeywordIntentClassifier
from src.agent.escalation import decide_escalation
from src.generation.generator import draft_reply
from src.generation.llm import generate_llm_reply

HIGH_CONFIDENCE = 0.75
MIN_RETRIEVAL_SCORE = 0.12

class SupportAgent:
    def __init__(self, retriever):
        self.classifier = KeywordIntentClassifier()
        self.retriever = retriever

    def respond(self, message):
        prediction = self.classifier.predict(message)
        evidence = self.retriever.search(message, k=3)
        top_score = evidence[0]["score"] if evidence else 0.0
        escalate, reason = decide_escalation(message, prediction["intent"], prediction["confidence"], top_score)
        deterministic_reply = draft_reply(
            message,
            prediction["intent"],
            evidence,
            escalate,
        )
        use_llm = (
            not escalate
            and prediction["confidence"] >= HIGH_CONFIDENCE
            and top_score >= MIN_RETRIEVAL_SCORE
        )
        llm_reply = (
            generate_llm_reply(message, prediction["intent"], evidence)
            if use_llm
            else None
        )
        return {
            **prediction,
            "draft_reply": llm_reply or deterministic_reply,
            "response_source": "llm" if llm_reply else "template",
            "llm_eligible": use_llm,
            "escalate": escalate,
            "escalation_reason": reason,
            "evidence": evidence,
        }
