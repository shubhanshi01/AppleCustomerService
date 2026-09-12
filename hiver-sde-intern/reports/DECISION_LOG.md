# Decision Log

This file records the important choices I made while building the AppleSupport support-agent prototype.

1. **I selected AppleSupport.** The dataset contains many AppleSupport messages and direct public support replies. This gave me enough examples to study common support problems without trying to support every brand.

2. **I treated conversation structure as part of the problem.** A customer message can depend on earlier messages. A reply is not useful evidence if it belongs to another branch of a Twitter conversation.

3. **I used `in_response_to_tweet_id` as the direct parent link.** The `response_tweet_id` field can contain several IDs, so it is not safe to treat it as one parent message.

4. **I did not repair missing threads by guessing.** I found 26 tweets whose parent context was outside the selected subset. Guessing the missing context could create a false conversation, so I record the issue instead.

5. **I chose a small intent taxonomy.** The system has eight broad intents. A small set is easier to explain, review, and label consistently than a large set of very similar categories.

6. **I kept an `other` intent.** Some tweets are too short or unclear to classify safely. It is better to admit uncertainty than force a detailed label.

7. **I used retrieval before reply generation.** The agent first looks for similar historical AppleSupport cases. This gives the reply process a reference point instead of asking it to make up a solution from the customer message alone.

8. **I do not copy historical replies directly.** Old Twitter replies may contain case-specific wording, private-message instructions, or stale links. The system uses them as evidence, then produces a conservative response template.

9. **I mark account and payment cases for escalation.** These cases may require identity checks or account information that public Twitter messages should not handle.

10. **I also escalate low-confidence and low-retrieval-score cases.** If the intent is unclear or no similar case is found, the system should not pretend to know the answer.

11. **I kept the first classifier simple.** The current keyword rules are easy to inspect. A more complex classifier should only be trained after the reviewed labels exist.

12. **I use a human-reviewed golden set for evaluation.** Weak keyword labels help sample examples, but they are not ground truth. The evaluation script blocks headline results until examples are reviewed.

13. **I include failure analysis in evaluation.** Accuracy alone would not reveal broken threads, unrelated retrieval evidence, or generic replies. Real failure examples are needed to understand risk.

14. **I prefer reliability over answering every message.** The prototype is designed to escalate when evidence is weak. A smaller number of safe answers is better than a larger number of unsupported answers.

15. **I will not report unmeasured results.** At this point, intent accuracy, retrieval quality, response grounding, and human agreement with an LLM judge are all `Not measured yet` because the golden labels have not been completed.
