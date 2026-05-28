"""
Day 1 — LLM API Foundation
AICB-P1: AI Practical Competency Program, Phase 1

Instructions:
    1. Fill in every section marked with TODO.
    2. Do NOT change function signatures.
    3. Copy this file to solution/solution.py when done.
    4. Run: pytest tests/ -v
"""

import os
import sys
import time
from typing import Any, Callable

# ---------------------------------------------------------------------------
# Estimated costs per 1K OUTPUT tokens (USD) — update if pricing changes
# ---------------------------------------------------------------------------
COST_PER_1K_OUTPUT_TOKENS = {
    "gpt-4o": 0.010,
    "gpt-4o-mini": 0.0006,
}

OPENAI_MODEL = "gpt-4o"
OPENAI_MINI_MODEL = "gpt-4o-mini"


# ---------------------------------------------------------------------------
# Task 1 — Call GPT-4o
# ---------------------------------------------------------------------------
def call_openai(
    prompt: str,
    model: str = OPENAI_MODEL,
    temperature: float = 0.7,
    top_p: float = 0.9,
    max_tokens: int = 256,
) -> tuple[str, float]:
    """
    Call the OpenAI Chat Completions API and return the response text + latency.
    """
    import openai

    client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    start = time.time()
    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        temperature=temperature,
        top_p=top_p,
        max_tokens=max_tokens,
    )
    latency = time.time() - start

    text = response.choices[0].message.content or ""
    # Guarantee a strictly positive latency for tests on very fast mocks.
    if latency <= 0:
        latency = 1e-6
    return text, latency


# ---------------------------------------------------------------------------
# Task 2 — Call GPT-4o-mini
# ---------------------------------------------------------------------------
def call_openai_mini(
    prompt: str,
    temperature: float = 0.7,
    top_p: float = 0.9,
    max_tokens: int = 256,
) -> tuple[str, float]:
    """
    Call the OpenAI Chat Completions API using gpt-4o-mini.
    """
    return call_openai(
        prompt,
        model=OPENAI_MINI_MODEL,
        temperature=temperature,
        top_p=top_p,
        max_tokens=max_tokens,
    )


# ---------------------------------------------------------------------------
# Task 3 — Compare GPT-4o vs GPT-4o-mini
# ---------------------------------------------------------------------------
def compare_models(prompt: str) -> dict:
    """
    Call both gpt-4o and gpt-4o-mini with the same prompt and return a
    comparison dictionary.
    """
    gpt4o_text, gpt4o_latency = call_openai(prompt)
    mini_text, mini_latency = call_openai_mini(prompt)

    # Rough token estimate: ~0.75 words per token
    estimated_tokens = len(gpt4o_text.split()) / 0.75
    gpt4o_cost_estimate = (estimated_tokens / 1000) * COST_PER_1K_OUTPUT_TOKENS["gpt-4o"]

    return {
        "gpt4o_response": gpt4o_text,
        "mini_response": mini_text,
        "gpt4o_latency": gpt4o_latency,
        "mini_latency": mini_latency,
        "gpt4o_cost_estimate": gpt4o_cost_estimate,
    }


# ---------------------------------------------------------------------------
# Task 4 — Streaming chatbot with conversation history
# ---------------------------------------------------------------------------
def streaming_chatbot() -> None:
    """
    Run an interactive streaming chatbot in the terminal.
    - Streams tokens as they arrive.
    - Keeps the last 3 conversation turns in history.
    - Exits when the user types 'quit' or 'exit'.
    """
    import openai

    client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    history: list[dict] = []

    print("Chatbot ready. Type 'quit' or 'exit' to end.")
    while True:
        try:
            user_input = input("You: ")
        except EOFError:
            break

        if user_input.strip().lower() in {"quit", "exit"}:
            print("Goodbye!")
            break

        history.append({"role": "user", "content": user_input})

        try:
            stream = client.chat.completions.create(
                model=OPENAI_MODEL,
                messages=history,
                stream=True,
            )
        except Exception as e:
            print(f"[error] {e}")
            history.pop()
            continue

        print("Assistant: ", end="", flush=True)
        assistant_reply = ""
        try:
            for chunk in stream:
                delta = chunk.choices[0].delta.content or ""
                print(delta, end="", flush=True)
                assistant_reply += delta
        except Exception as e:
            print(f"\n[stream error] {e}")
        print()

        history.append({"role": "assistant", "content": assistant_reply})

        # Keep only the last 3 turns (one turn = user + assistant = 2 messages)
        if len(history) > 6:
            history = history[-6:]


# ---------------------------------------------------------------------------
# Bonus Task A — Retry with exponential backoff
# ---------------------------------------------------------------------------
def retry_with_backoff(
    fn: Callable,
    max_retries: int = 3,
    base_delay: float = 0.1,
) -> Any:
    """
    Call fn(). On exception, retry up to max_retries with exponential backoff.
    Re-raises the last exception when all retries are exhausted.
    """
    last_exc: Exception | None = None
    for attempt in range(max_retries + 1):
        try:
            return fn()
        except Exception as e:
            last_exc = e
            if attempt >= max_retries:
                break
            time.sleep(base_delay * (2 ** attempt))
    assert last_exc is not None
    raise last_exc


# ---------------------------------------------------------------------------
# Bonus Task B — Batch compare
# ---------------------------------------------------------------------------
def batch_compare(prompts: list[str]) -> list[dict]:
    """
    Run compare_models on each prompt and add the original prompt to the result.
    """
    results: list[dict] = []
    for prompt in prompts:
        result = compare_models(prompt)
        result["prompt"] = prompt
        results.append(result)
    return results


# ---------------------------------------------------------------------------
# Bonus Task C — Format comparison table
# ---------------------------------------------------------------------------
def format_comparison_table(results: list[dict]) -> str:
    """
    Format comparison results as a readable text table.
    """
    def truncate(text: str, width: int = 40) -> str:
        text = str(text).replace("\n", " ")
        return text if len(text) <= width else text[: width - 1] + "…"

    headers = ["Prompt", "GPT-4o Response", "Mini Response", "GPT-4o Latency", "Mini Latency"]
    rows = [headers]
    for r in results:
        rows.append([
            truncate(r.get("prompt", "")),
            truncate(r.get("gpt4o_response", "")),
            truncate(r.get("mini_response", "")),
            f"{r.get('gpt4o_latency', 0):.3f}s",
            f"{r.get('mini_latency', 0):.3f}s",
        ])

    widths = [max(len(row[i]) for row in rows) for i in range(len(headers))]
    sep = "+".join("-" * (w + 2) for w in widths)
    sep = f"+{sep}+"

    def fmt_row(row):
        cells = [f" {row[i]:<{widths[i]}} " for i in range(len(headers))]
        return "|" + "|".join(cells) + "|"

    lines = [sep, fmt_row(rows[0]), sep]
    for row in rows[1:]:
        lines.append(fmt_row(row))
    lines.append(sep)
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Entry point for manual testing
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    test_prompt = "Explain the difference between temperature and top_p in one sentence."
    print("=== Comparing models ===")
    result = compare_models(test_prompt)
    for key, value in result.items():
        print(f"{key}: {value}")

    print("\n=== Starting chatbot (type 'quit' to exit) ===")
    streaming_chatbot()


# ---------------------------------------------------------------------------
# Register a hyphen-free module alias so unittest.mock.patch can resolve us.
# (The folder name "Day01-lab-assignment" contains a hyphen, which is not a
# valid Python identifier and breaks pkgutil.resolve_name used by patch().)
# ---------------------------------------------------------------------------
_alias = "day01_template"
if _alias not in sys.modules:
    sys.modules[_alias] = sys.modules[__name__]
for _fn in (
    call_openai,
    call_openai_mini,
    compare_models,
    streaming_chatbot,
    retry_with_backoff,
    batch_compare,
    format_comparison_table,
):
    _fn.__module__ = _alias