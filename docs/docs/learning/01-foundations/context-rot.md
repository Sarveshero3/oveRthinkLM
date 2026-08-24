# Context Rot

## What it is

When you paste a really long document into an LLM and ask a question about it, the model's answer quality gets worse — even if the document is technically within the model's "context window" limit.

GPT-5 might say it can handle 1 million tokens. But if you actually give it 500,000 tokens and ask "what's in paragraph 847?", it will often get it wrong. The information is *there* in the input, but the model can't reliably access it.

This degradation is called **context rot**.

## Why it happens

LLMs process text through an "attention mechanism" — the model assigns weights to every token in the input when generating each output token. As the input gets longer:

1. **Attention gets diluted** — each token has to compete with more neighbors for the model's "attention budget"
2. **Positional encoding degrades** — the model's sense of "where" things are in the text becomes less reliable at positions far from the beginning
3. **Information gets compressed** — the model's internal representation can only hold so much, so details get lost

## The key insight

Context rot isn't a bug that will be fixed by making context windows bigger. It's a fundamental limitation of how current transformers process information. Making the window bigger just means the rot starts further out — it doesn't eliminate it.

This is why RLMs exist: instead of cramming everything into the window and hoping, they let the model *programmatically explore* the data, only pulling in what it needs.

## Concrete example

Imagine you have a 200-page corporate report and you ask: "How many times was Project Alpha mentioned across all quarterly summaries?"

- **Without RLM (vanilla LLM):** You paste all 200 pages into the prompt. The model reads everything at once. Due to context rot, it might count 3 mentions when there were actually 7 — it just didn't "see" the ones in the middle of the document where attention was weakest.

- **With RLM:** The model gets told "you have a 200-page document in variable `corpus`. Use Python to find what you need." The model writes `corpus.count("Project Alpha")` or slices specific sections to read them carefully. It never needs to hold all 200 pages in its attention at once.

## Why this matters for our project

The entire research question hinges on context rot:
- RLMs claim to solve it through programmatic exploration
- But the reproduction study found that exploration itself can cause *new* problems (format collapse, latency blowup)
- And Apple's SRLM paper claims you can get the same benefit through smarter program selection without even recursing

Our project tests all three claims empirically.
