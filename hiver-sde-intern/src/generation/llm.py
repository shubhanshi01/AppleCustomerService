"""Optional LLM response generation grounded in retrieved support examples."""

import json
import os
from urllib import request


def generate_llm_reply(message, intent, evidence):
    """Return a grounded LLM draft, or None when LLM generation is unavailable."""
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key or not evidence:
        return None

    endpoint = os.getenv(
        "GROQ_BASE_URL",
        "https://api.groq.com/openai/v1/chat/completions",
    )
    model = os.getenv("GROQ_MODEL", "llama-3.1-8b-instant")
    historical_examples = "\n\n".join(
        f"Customer: {item['customer_text']}\n"
        f"Historical support reply: {item['historical_reply']}"
        for item in evidence
    )
    payload = {
        "model": model,
        "temperature": 0.2,
        "messages": [
            {
                "role": "system",
                "content": (
                    "You draft concise, safe public customer-support replies. "
                    "Use only the historical examples as grounding. Do not claim "
                    "to access accounts, invent policy, or ask the customer to "
                    "share passwords, payment details, or private data. "
                    "Do not mention that you used historical examples."
                ),
            },
            {
                "role": "user",
                "content": (
                    f"Intent: {intent}\nCustomer message: {message}\n\n"
                    f"Historical examples:\n{historical_examples}\n\n"
                    "Write one helpful reply in 2-4 sentences. If the examples "
                    "do not support a concrete step, ask one focused clarification "
                    "question instead."
                ),
            },
        ],
    }
    req = request.Request(
        endpoint,
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        method="POST",
    )
    try:
        with request.urlopen(req, timeout=20) as response:
            result = json.loads(response.read().decode("utf-8"))
        content = result["choices"][0]["message"]["content"].strip()
        return content or None
    except (OSError, KeyError, IndexError, TypeError, ValueError, json.JSONDecodeError):
        return None