HIGH_RISK = ("hacked", "fraud", "unauthorized", "stolen", "legal", "sue", "death", "emergency", "personal data")

def decide_escalation(text, intent, confidence, retrieval_score):
    message = (text or "").lower()
    matched = next((term for term in HIGH_RISK if term in message), None)
    if matched:
        return True, f"Sensitive or high-risk signal: '{matched}'."
    if intent in {"account_and_security", "billing_and_purchase"}:
        return True, "Account or payment issue needs identity-aware support."
    if confidence < 0.45:
        return True, "Intent confidence is below the auto-handle threshold."
    if retrieval_score < 0.12:
        return True, "No sufficiently similar resolved historical case was found."
    return False, "Clear, low-risk issue with relevant historical resolution evidence."
