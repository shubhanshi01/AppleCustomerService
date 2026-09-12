# Failure Analysis

## Why this section exists

This project uses real Twitter support data. The data is useful, but it is not clean or complete. I found problems in the conversation structure before I used the data for retrieval. I am documenting them because they can lead to a confident-looking but wrong support reply.

## Missing thread context

While reconstructing AppleSupport conversations from a development sample, I found 26 tweets that did not receive a `thread_id` under the first version of the reconstruction logic. Their parent tweet was not present in the selected AppleSupport subset.

This does not mean the tweets are invalid. It means that their earlier context is missing from the data used by the reconstruction step. For example, a support tweet can point to a customer tweet outside the sample. The support tweet is then a local start of the available data, but it is not the real start of the original conversation.

I do not repair these threads by guessing what the missing message said. Guessing could join unrelated messages and create false training or retrieval examples. Instead, I record the missing context as a data-quality issue.

## Why incomplete threads are dangerous for retrieval

Retrieval should return a past case that is similar to the new customer message. If a past thread is incomplete, the retrieved reply may depend on information that is not visible. For example, it may refer to an earlier troubleshooting step, an order number, or a private conversation.

Using that reply as evidence can cause two problems:

1. The system may recommend a step that does not fit the new customer's issue.
2. The system may look grounded because it found a historical reply, even though the visible evidence is incomplete.

The current retrieval builder uses only direct customer-to-AppleSupport reply pairs. This reduces branch-mixing, but it does not prove that the full original conversation is available. I should not describe the current retrieval corpus as fully reconstructed threads.

## Real failure cases

| Case | Expected behavior | Actual behavior | Why it failed | Severity | Possible improvement |
| --- | --- | --- | --- | --- | --- |
| 26 tweets with missing thread context | Keep the message only when its available context is clear; flag incomplete context. | The first reconstruction logic left the tweets without `thread_id`. | Their parent tweet was outside the selected subset. | High | Keep an `incomplete_context` flag and do not use flagged examples for evidence-sensitive evaluation. |
| Announcement root with many replies | Treat each customer branch as a separate support issue. | One root component contained 37 tweets and 11 unrelated customer branches. | A connected Twitter component is not always one conversation. | High | Follow direct parent-child links and create branch-level examples. |
| Multiple values in `response_tweet_id` | Use one reliable parent relationship. | Some values contained several tweet IDs; one had 1,090 IDs in the development sample. | This field represents outgoing links and is not a single-parent field. | High | Use `in_response_to_tweet_id` for the direct parent when it is available. |
| Short or link-only messages | Preserve the message and use surrounding context when available. | 36 cleaned texts became empty in the reconstructed AppleSupport data. | Cleaning removed mentions and URLs, leaving little visible text. | Medium | Keep raw text, a quality flag, and context rather than deleting the row. |
| Follow-up messages without `@AppleSupport` | Keep valid follow-up messages that belong to an AppleSupport conversation. | A direct-mention filter missed 731 customer tweets in the reconstructed sample. | Customers often mention the brand only in the first message. | Medium | Use conversation links as well as direct mentions when building analysis data. |
| Non-English or very short messages | Avoid pretending the system understands them well. | Language detection can be unreliable for short messages, and some support replies explicitly ask users to contact support in another language. | Short text provides weak language evidence. | Medium | Use language as a flag, not a hard filter; escalate when the message is unclear. |
| Keyword ambiguity | Route the message to the right intent. | Words such as "charge" can mean a payment issue or charging a device. | The current intent classifier uses simple keyword rules. | Medium | Review ambiguous examples in the golden set and train a classifier only on reviewed labels. |
| Generic generated reply | Give a next step that matches the retrieved case. | Current templates are safe but can be general, and they do not copy a specific action from retrieval evidence. | The response generator is intentionally constrained but is not yet evidence-conditioned. | Medium | Add a checked evidence-to-response step and measure whether reviewers consider each reply supported. |

## How the system handles failures now

- It uses direct `in_response_to_tweet_id` links for customer-to-support pairs instead of treating a whole root component as one conversation.
- It escalates account, payment, privacy, fraud, legal, low-confidence, and low-retrieval-score messages.
- It keeps a simple response template instead of copying old public replies that may contain outdated links or case-specific instructions.
- It does not report evaluation metrics until the golden-set labels have been reviewed.

These controls reduce risk, but they do not solve every problem. Retrieval quality: Not measured yet. Response grounding: Not measured yet. Escalation quality against human labels: Not measured yet.

## What I learned

The main lesson is that support data is not a clean question-and-answer dataset. Twitter conversations are graphs with branches, missing parents, replies that move to direct messages, and short messages that need context. A simple model on the wrong conversation structure can look good in a demo and still be unsafe in practice.

For this reason, I prefer a smaller system that escalates uncertain cases over a system that tries to answer every message. The next important work is to review the golden set, measure the system on those reviewed examples, and inspect failures by hand.
