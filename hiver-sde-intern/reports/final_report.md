# AppleSupport replay agent report

## Problem framing

The agent handles the first public response to an AppleSupport mention. A good response recognizes the operational issue, gives a useful public-safe next step, and routes cases requiring identity, payment, privacy, or judgment to a human. It does not attempt account lookups, refunds, repair diagnosis, authentication, or private-DM workflows. The source is public Twitter data, so this is a replay evaluation rather than proof of production performance.

## System

The pipeline creates 106,622 immediate customer-to-AppleSupport resolution pairs from the supplied `twcs.csv`. It routes into eight intents: account/security, billing/purchase, device hardware, software/update, service/connectivity, how-to/setup, order/repair, and other. It retrieves three historical public resolutions with TF-IDF, drafts a constrained response, and escalates high-risk, uncertain, or poorly-covered messages. The UI exposes the retrieved evidence and the routing reason.

## Evaluation design

The golden set is a 180-example stratified annotation worksheet (144 test / 36 dev). A human reviewer must label intent, escalation, escalation reason, and reply quality before any headline score is allowed. Intent is measured with accuracy and macro-F1; escalation with precision, recall, F1, and accuracy. Reply quality uses a four-axis LLM rubric: groundedness, helpfulness, safety, and tone. Before relying on that judge, double-score at least 30 random examples with a human and report exact agreement and Cohen's kappa.

## Results

No headline metric is reported yet. The worksheet is intentionally unreviewed, and treating keyword-derived sampling labels as human ground truth would be misleading. The reproducible operational result is 106,622 direct resolution pairs created from the local export. After annotation, compare three systems on the same frozen test set: (1) always-other / always-escalate fixed reply, (2) keyword routing plus fixed reply, and (3) the proposed retrieval-plus-policy agent.

## Failure analysis

See `failure_analysis.txt` for raw-data examples. The highest-risk failure modes are: disconnected or announcement-root conversation branches; multi-ID `response_tweet_id` values; parents outside a sample; short/URL-only tweets that lose meaning without context; and unreliable language detection on short messages. Additional system-level risks are keyword ambiguity ("charge" can mean power or billing), stale historical links, retriever lexical mismatch, and templates that may be too generic. The policy turns ambiguity and missing evidence into escalation rather than a confident public reply.

## What is misleading about my headline number?

106,622 is retrieval-corpus size, not accuracy. Any intent score made from weak keyword labels would measure agreement with its own heuristic, not quality. A public Twitter reply is also not a verified successful resolution, and direct reply pairs omit cases that moved to private support. Finally, the sample over-represents frequent software/update language, so micro accuracy could conceal poor rare-intent performance; macro-F1 and the stratified golden review are required.

## One more week

Complete blinded dual annotation and adjudication; train/calibrate a TF-IDF or embedding classifier on the reviewed dev split; add semantic retrieval and a contradiction/PII guard; evaluate by intent, message length, language, and risk group; and conduct a small red-team suite for payment, account takeover, privacy, and unsafe troubleshooting prompts.
