# AppleSupport replay agent

An offline-first support-agent prototype built on the Customer Support on Twitter dataset. It classifies messages into eight AppleSupport-specific operational intents, retrieves similar historical AppleSupport resolutions, drafts a conservative public reply, and either auto-handles or escalates with an explicit reason.

## Recruiter quick read

**What is built:** an end-to-end AppleSupport chatbot with interpretable intent routing, TF-IDF retrieval, policy-based escalation, evidence display, and an optional Groq LLM response layer.

**Verified project outputs:**

- `106,622` immediate customer-to-AppleSupport resolution pairs built from the supplied export.
- `180` stratified golden-set examples created for human review (`144` test / `36` dev).
- `4` automated tests passing for data contracts, intent routing, retrieval, and agent behavior.
- Streamlit UI exposes intent, confidence, route, escalation reason, draft response, response source, and retrieved evidence.

**Evaluation honesty:** headline quality metrics are intentionally not reported yet because the golden worksheet is not human-reviewed. Weak keyword labels are used for sampling only, not as ground truth. The evaluation scripts print `Not measured yet` until reviewed rows are available.

**Start here:** [final report](reports/final_report.md) | [decision log](reports/decision.txt) | [failure analysis](reports/failure_analysis.txt) | [evaluation notebook](notebooks/06_evaluation_analysis.ipynb)

**Submission scope:** AppleSupport was selected as the brand. The system is a public-Twitter replay prototype, not a production account-support tool. It does not access accounts, process payments, diagnose hardware remotely, or send messages.

## System at a glance

```text
Customer message
	|
	v
Keyword intent classifier (8 operational intents)
	|
	+--> risk/confidence policy ----> auto-handle or escalate with reason
	|
	v
TF-IDF retrieval of historical customer -> AppleSupport replies
	|
	+--> deterministic safe template
	|
	+--> optional Groq LLM rewrite when confidence and evidence are strong
```

The LLM is never used for escalated or low-confidence cases. If Groq is not configured or the request fails, the local deterministic template remains the fallback.

## Scope

This is a public-Twitter replay prototype, not a production Apple agent. It deliberately does not access accounts, process refunds, diagnose hardware remotely, make policy promises, or send messages. Account, payment, privacy, fraud, legal, and low-confidence cases are escalated.

## Reproduce (under 15 minutes)

Prerequisite: place Kaggle's `twcs.csv` at `data/raw/twcs.csv` (the repository intentionally does not commit the source data).

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python scripts\build_retrieval_index.py
python scripts/build_golden_set.py  # only if data/golden/apple_golden.csv is absent
streamlit run app\streamlit_app.py
```

The index build scans the local CSV and writes `data/processed/apple_reply_pairs.csv`. On the supplied export it produces 106,622 immediate customer-to-AppleSupport pairs. The Streamlit app runs locally and shows the intent, confidence, route, reply, and retrieved evidence.

Run the automated checks from the repository root:

```powershell
python -m pytest -q
```

### Optional Groq response generation

For high-confidence, non-escalated messages with relevant historical evidence, the app can use Groq's OpenAI-compatible API to improve the draft reply. Without a key, it automatically uses the deterministic local template.

```powershell
$env:GROQ_API_KEY = "your-groq-api-key"
$env:GROQ_MODEL = "llama-3.1-8b-instant"
streamlit run app\streamlit_app.py
```

The key is read at runtime and is never written to the repository. The UI labels whether each response came from `llm` or the local `template` fallback.

For a safe configuration template, copy `.env.example` into your local environment. Do not commit `.env` or API keys.

## Evaluation protocol

`scripts/build_golden_set.py` creates a stratified 180-row worksheet at `data/golden/apple_golden.csv`: 144 test / 36 dev, with over-sampling of rare weak-label buckets. A reviewer labels `gold_intent`, `gold_escalate`, an escalation reason, and a 1-5 reply score, then sets `reviewed=True`. The worksheet includes the historical reply only for annotation context; it is not an input to the classifier. Do not run this script again after annotation because it creates a fresh worksheet.

```powershell
python scripts\prepare_evaluation.py
python scripts\evaluate.py
```

`prepare_evaluation.py` excludes all golden-set tweets from retrieval before creating `data/evaluation/apple_predictions.csv`. Review the top retrieval result and generated reply in that file, then run `evaluate.py`. The evaluator prints `Not measured yet` for any field that has not been reviewed. Weak labels are useful for sampling but cannot be presented as human gold. Intent metrics are accuracy and macro-F1; reply quality is reviewed for relevance, grounding, and helpfulness. Double-score a random 30+ replies with a human and the judge, then use `human_agreement.agreement` to report exact agreement and Cohen's kappa.

## Baselines

1. Trivial: always classify `other`, always escalate, and send a fixed `Please contact Apple Support` reply.
2. Simple: keyword intent routing plus the same fixed reply.
3. Proposed: keyword intent routing, TF-IDF retrieval of historical AppleSupport resolutions, constrained response templates, and risk/coverage escalation.

The current routing classifier is intentionally interpretable. A next iteration can train `TfidfIntentClassifier` on the reviewed development split, then compare it with the keyword baseline on the held-out golden test split.

## Deliverables map

- **Runnable pipeline:** `scripts/build_retrieval_index.py`, `src/agent`, `src/retrieval`, and `app/streamlit_app.py`
- **Golden evaluation set:** `data/golden/apple_golden.csv`, generated by `scripts/build_golden_set.py`
- **Evaluation harness:** `scripts/prepare_evaluation.py`, `scripts/evaluate.py`, and `src/evaluation`
- **LLM-as-judge support:** `src/evaluation/llm_judge.py`; human agreement utilities are in `src/evaluation/human_agreement.py`
- **Analysis notebooks:** `notebooks/01_dataset_exploration.ipynb` through `notebooks/06_evaluation_analysis.ipynb`
- **Report and decisions:** `reports/final_report.md`, `reports/decision.txt`, and `reports/failure_analysis.txt`

## Project layout

- `src/agent`: decision flow and escalation policy
- `src/intent`: taxonomy, keyword baseline, optional TF-IDF classifier
- `src/retrieval`: historical-reply retrieval
- `scripts`: dataset build, golden worksheet build, and evaluation
- `reports/REPORT.md`: submission report
- `reports/FAILURE_ANALYSIS.md`: data and system failures
- `reports/DECISION_LOG.md`: design decisions

## Data and attribution

Primary data: [Customer Support on Twitter](https://www.kaggle.com/datasets/thoughtvector/customer-support-on-twitter), published by Thought Vector. Product names and historical public replies remain the property of their respective owners. This project uses the data only for the take-home prototype.
