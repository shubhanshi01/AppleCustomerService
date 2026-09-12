import sys
from pathlib import Path
import pandas as pd
import streamlit as st

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from src.config import PROCESSED
from src.retrieval.retriever import ReplyRetriever
from src.agent.pipeline import SupportAgent

st.set_page_config(page_title="AppleSupport replay", layout="wide")
st.title("AppleSupport reply assistant")
st.caption("Offline prototype using retrieved historical public support replies. It does not access customer accounts.")

@st.cache_resource
def load_agent():
    pairs = pd.read_csv(PROCESSED / "apple_reply_pairs.csv")
    pairs = pairs.dropna(subset=["customer_text", "support_reply"])
    return SupportAgent(ReplyRetriever(pairs))

if not (PROCESSED / "apple_reply_pairs.csv").exists():
    st.warning("Build the retrieval data first: `python scripts/build_retrieval_index.py`")
    st.stop()

message = st.text_area("Customer message", placeholder="My iPhone keeps restarting after the update")
if st.button("Draft reply", type="primary", disabled=not message.strip()):
    result = load_agent().respond(message)
    a, b, c = st.columns(3)
    a.metric("Intent", result["intent"].replace("_", " "))
    b.metric("Confidence", f"{result['confidence']:.0%}")
    c.metric("Route", "Escalate" if result["escalate"] else "Auto-handle")
    st.subheader("Draft")
    st.caption(f"Response source: {result['response_source']}")
    st.write(result["draft_reply"])
    st.info(result["escalation_reason"])
    st.subheader("Historical evidence")
    st.dataframe(pd.DataFrame(result["evidence"]), use_container_width=True, hide_index=True)
