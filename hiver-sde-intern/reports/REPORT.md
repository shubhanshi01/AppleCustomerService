# AppleSupport AI Support Agent

## 1. Problem

The goal of this project is to build a small AI support agent for AppleSupport messages from Twitter. The agent should identify the type of customer problem, find similar historical AppleSupport replies, draft a safe public reply, and decide whether the case should be handled automatically or sent to a human.

For this project, a good answer is not just a polite answer. It should match the customer's problem, avoid making up account information or policies, and escalate when the available evidence is weak.

## 2. Dataset

I used the Customer Support on Twitter dataset from Kaggle (`thoughtvector/customer-support-on-twitter`). It contains public customer-support conversations from different brands. I used the local `twcs.csv` export.

The raw data is noisy. Twitter conversations can have branches, messages can point outside a selected sample, and some replies ask the customer to continue in a direct message. This means the data cannot be treated as a simple question-and-answer table.

## 3. Brand selection

I selected AppleSupport. The dataset has enough AppleSupport messages and direct public replies to build a focused prototype. AppleSupport messages also cover different support topics, such as software updates, device issues, billing, account access, and orders.

## 4. Data cleaning and conversation structure

I kept the raw message text and used cleaned text only as supporting data. I did not remove short messages automatically because a short reply can still make sense when its parent message is available.

The most important data step was checking conversation structure. I found that a root Twitter component can contain several unrelated customer branches. I also found 26 tweets where earlier thread context was missing from the selected subset. I did not guess the missing messages. I record these rows as incomplete-context cases because guessing could create false conversations.

The retrieval data is built from direct customer-to-AppleSupport reply pairs using `in_response_to_tweet_id`. This is safer than treating a whole component as one conversation, but it still does not prove that every full original thread is available.

## 5. Intent classification

I defined eight intents:

- account and security
- billing and purchase
- device hardware
- software and update
- service and connectivity
- how-to and setup
- order and repair
- other

The current classifier uses clear keyword rules. This is a simple starting point that is easy to inspect. The project also includes a TF-IDF classifier that can be trained later using reviewed labels. I did not train or report a learned model using weak labels because that would not be a fair evaluation.

## 6. Retrieval

The retrieval step uses TF-IDF to find customer messages that are similar to a new message. The local data build created 106,622 direct customer-to-AppleSupport reply pairs from the supplied export.

The historical reply is shown as evidence in the application. It is not copied directly into the new reply because old replies may contain outdated links, private-message instructions, or details that only apply to one customer.

## 7. Response generation

The current reply generator uses short, conservative templates. It gives general next steps and directs sensitive cases to Apple Support. This design reduces the chance of making an unsupported promise.

There is an important limitation: the current template generator does not yet turn a specific retrieved step into a specific response. Therefore, it should not be described as fully grounded generation. Response grounding: `Not measured yet`.

## 8. Routing and escalation

The system escalates messages about accounts, payments, privacy, fraud, legal issues, and other high-risk terms. It also escalates when the intent confidence is low or the best retrieval score is low.

This choice is deliberate. The agent should not try to answer every message. A safe escalation is better than a confident but unsupported reply.

## 9. Evaluation methodology

I created a 180-row golden-set worksheet with 36 development rows and 144 test rows. The worksheet is sampled across the weak intent buckets so that rare categories are not ignored.

A reviewer must label the intent, whether the case should escalate, and a reply-quality score. The evaluation process then:

1. Excludes all golden-set tweets from the retrieval index to avoid retrieving the same historical pair.
2. Creates a prediction file with the predicted intent, route, draft reply, top retrieved case, and score.
3. Lets a reviewer mark whether the top retrieved case is relevant and whether the reply is grounded.
4. Calculates metrics only when the needed human-review fields are present.

The project also includes an LLM-judge rubric for groundedness, helpfulness, safety, and tone. Before using an LLM judge as a result, it should be compared with human scores on at least 20 double-scored examples.

## 10. Results

Intent accuracy: `Not measured yet`.

Intent macro-F1: `Not measured yet`.

Retrieval top-1 relevance: `Not measured yet`.

Response grounding rate: `Not measured yet`.

Response helpfulness: `Not measured yet`.

Escalation accuracy: `Not measured yet`.

The 106,622 number is the size of the retrieval corpus. It is not an accuracy or quality result.

## 11. Failure analysis

The main failures found so far are incomplete threads, unrelated branches below an announcement tweet, multiple IDs in `response_tweet_id`, short or URL-heavy messages, follow-up messages that do not mention AppleSupport again, and language uncertainty.

The detailed cases and a severity table are in [FAILURE_ANALYSIS.md](FAILURE_ANALYSIS.md). The most important finding is that incorrect conversation grouping can contaminate retrieval evidence before the model makes any decision.

## 12. Misleading numbers

Some numbers can look good while hiding a problem.

- High intent accuracy does not automatically mean good support. A classifier can label a message correctly while the reply is unhelpful or unsafe.
- Accuracy on weak labels would only show agreement with the rule used to create those labels. It would not show agreement with a human reviewer.
- A good-looking generated reply can still be unsupported. It may sound polite but recommend a step that is not supported by the retrieved evidence.
- A high retrieval similarity score does not prove a useful result. A retrieved historical reply can depend on missing thread context or can simply redirect the customer to direct messages.
- Escalation accuracy matters because a support agent can be dangerous in two opposite ways: it can escalate nearly everything, or it can fail to escalate sensitive cases.
- Micro averages can hide weak performance on rare intents. Macro-F1 and per-intent review are important after enough examples are labelled.

## 13. Limitations

This is a replay prototype using public Twitter data. It does not have customer account access, current Apple policies, verified resolution outcomes, or private-message context. It also uses simple keyword intent rules and lexical retrieval. The golden set has been created but is not yet reviewed, so no quality claims should be made.

## 14. Future improvements

The next step is to complete the reviewed golden set and inspect errors. After that, I would train a simple classifier on reviewed development data, add better semantic retrieval, add an evidence check before drafting a reply, and test difficult account, billing, privacy, and multi-intent messages.

I would also keep incomplete-context examples separate and compare results with and without them. This would show how much missing thread context affects retrieval and reply quality.

## 15. Final conclusion

The project shows a working support-agent pipeline, but the most important work is still evaluation. The data analysis found real conversation-structure problems that could otherwise make the system look stronger than it is. My main design choice is to be conservative: use historical evidence when it is available, show that evidence to the reviewer, and escalate when the message or evidence is unclear.
