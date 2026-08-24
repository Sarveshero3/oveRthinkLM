# Paper 1: "Recursive Language Models" — Zhang, Kraska, Khattab (MIT CSAIL, Dec 2025)

**arXiv:** 2512.24601  
**Reference code:** `github.com/alexzhang13/rlm` (design reference only, never import)

## What they proposed

This is the original paper that invented the RLM concept. The core idea:

> Instead of feeding the entire document to the LLM, store it in a Python REPL as a variable and let the model write code to explore it programmatically — including recursively calling itself on subsets.

## Key claims

1. **RLMs handle near-infinite context** — by never putting the full document in the attention window, context rot is avoided entirely.

2. **RLMs outperform vanilla LLMs** on long-context benchmarks (OOLONG, S-NIAH) using the same underlying model.

3. **Cost stays comparable** to a single LLM call on average — the model doesn't always recurse; when the question is simple, it answers directly.

4. **No retraining needed** — the REPL scaffold works with any off-the-shelf LLM (though fine-tuning helps).

## What they built

- A Python REPL environment where `corpus_str` holds the document
- A `llm_query(text, question)` function for recursive sub-calls
- Support for multiple sandbox backends (local `exec`, Docker, Modal cloud sandboxes)
- Benchmarks on OOLONG (complex reasoning) and S-NIAH (simple retrieval)

## What they used for models

- GPT-5 (frontier at time of publication)
- Qwen3-8B (fine-tuned to be "RLM-native" — out of our scope)

## Our relationship to this paper

We are building the same mechanism from scratch to understand it deeply, not importing their code. Their implementation tells us *what* the REPL environment should look like, what functions should be available, and what the system prompt should say. We read it for design reference, not as a dependency.
