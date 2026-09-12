import pandas as pd
from src.agent.pipeline import SupportAgent
from src.retrieval.retriever import ReplyRetriever

def test_agent_returns_auditable_contract():
    data = pd.DataFrame({"customer_text": ["my iphone update crashes", "how do I set this up"], "support_reply": ["Try updating your iPhone.", "Here are setup steps."]})
    result = SupportAgent(ReplyRetriever(data)).respond("my iphone update crashes")
    assert result["intent"] == "software_and_update"
    assert isinstance(result["escalate"], bool)
    assert result["draft_reply"]
    assert len(result["evidence"]) == 2
