# Paper 3: "Recursive Language Models Meet Uncertainty" — Apple Research (Mar 2026)

**arXiv:** 2603.15653  
**Reference code:** NONE — no public implementation exists anywhere. We build this from the paper alone.

## What they proposed

Apple researchers said: "Wait — maybe the recursive sub-calls aren't even the important part of RLM. Maybe what matters is just *choosing a good exploration strategy*, which you can do without recursion."

They introduced **SRLM** (Self-Reflective Program Search for Long Context).

## How SRLM works (step by step)

### Step 1: Generate multiple candidate programs

Instead of having the model write one exploration program and run it, SRLM asks the model to generate **N different approaches** (e.g., N=5):

```
Program A: Split document by chapters, search each for keywords
Program B: Use regex to find all dollar amounts, sum them
Program C: Read first and last 1000 chars, infer structure, then target-search
Program D: Binary search through document by character offset
Program E: Extract all headers, pick relevant ones, read those sections
```

Each program is a different strategy for answering the same question about the same document.

### Step 2: Execute all candidates

Run each program in the REPL. Each produces a candidate answer.

### Step 3: Score each candidate using three uncertainty signals

This is the key innovation. Instead of just picking the first answer, SRLM evaluates *how confident* the model is in each answer using three signals:

1. **Self-Consistency** — Run each program multiple times (with sampling temperature > 0). If the answer is the same every time, the model is confident. If it changes, the model is uncertain.

2. **Verbalized Confidence** — Ask the model: "On a scale of 0-100, how confident are you in this answer?" Models can often tell you when they're guessing.

3. **Reasoning Length** — If the model produces a short, concise answer, it's probably confident. If it produces a long, hedging, qualification-filled answer, it's probably uncertain. (Counterintuitive but empirically validated.)

### Step 4: Pick the winner

Combine the three signals into a composite score. The candidate with the highest confidence gets selected as the final answer.

## Key insight: no recursion needed

SRLM never calls `llm_query()` — no sub-LLM calls at all. It explores the document with Python code (like RLM does), but instead of recursing deeper when it's not sure, it *tries multiple approaches at the same level and picks the most confident one*.

## Their results

- SRLM matches or beats depth-1 RLM on most tasks
- Up to **22% improvement over RLM** under the same time budget
- More consistent — less high-variance behavior than recursive approaches
- Works for both short and long contexts (RLM sometimes *hurts* on short contexts)

## Why this matters for us

1. **SRLM is our 4th configuration** — we need to build it from scratch since there's no public code
2. **The uncertainty signals are the bridge to the hybrids** — Hybrid-1 and Hybrid-2 take these exact signals and apply them *inside* a recursive RLM, which nobody has tried
3. **If SRLM alone matches depth-1 RLM**, that validates Apple's claim that recursion isn't the key driver — the key driver is program selection quality
