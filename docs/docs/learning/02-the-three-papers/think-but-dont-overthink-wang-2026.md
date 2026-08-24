# Paper 2: "Think, But Don't Overthink" — Wang (Mar 2026)

**arXiv:** 2603.02615  
**Reference code:** `github.com/drbillwang/rlm-reproduction` (design reference only, never import)

## What they did

This is a **reproduction study**. Wang took the original RLM idea and tested it more carefully, finding that the benefits are much more nuanced than the original paper suggested.

## Key findings

### 1. Depth-1 helps complex reasoning but hurts simple retrieval

This is the central "don't overthink" finding:

| Task type | Depth-0 (vanilla) | Depth-1 (RLM) | Verdict |
|-----------|-------------------|----------------|---------|
| **Complex reasoning** (counting, aggregation over long text) | 0.0% accuracy | 42.1% accuracy | ✅ Massive improvement |
| **Simple retrieval** (find a specific fact in long text) | 100% accuracy | Lower | ❌ Worse than doing nothing |

Why? For simple retrieval, the vanilla LLM can just scan the full context and find the needle. When you add the RLM scaffold, the model wastes time writing code to explore when it could have just answered. The overhead introduces errors.

### 2. Depth-2 makes everything worse

Going from depth-1 to depth-2 caused:
- **Accuracy drops** — 100% → 70% on some tasks
- **Latency explosion** — 3.6 seconds → 344.5 seconds (96× slower)
- **Format collapse** — The model starts emitting raw Python `print()` statements instead of actual answers

### 3. Three specific failure modes at depth-2

1. **Format collapse:** The sub-sub-model gets confused about what it's supposed to output. It's inside a REPL inside a REPL, and it starts printing code instead of answers.

2. **Parametric hallucination:** The deeper model abandons the provided text and starts making up facts from its training data instead.

3. **Performative reasoning / endless loops:** The model spawns redundant sub-calls that don't contribute to the answer, generating verbose explanations instead of converging.

## What models they used

- **DeepSeek v3.2** — one of the two main test models
- **Kimi K2** — the other main test model (available on Groq)

## Why this matters for us

This paper defines two of our six configurations:
- **Depth-1 RLM** — expected to help complex tasks, hurt simple ones
- **Depth-2 RLM** — expected to cause format collapse and latency blowup

We test whether we can reproduce these exact findings. More importantly, our Hybrid-2 configuration asks: *can SRLM's uncertainty signals prevent the depth-2 failures?* If Hybrid-2 avoids format collapse while keeping depth-2's theoretical power, that's a real result.
