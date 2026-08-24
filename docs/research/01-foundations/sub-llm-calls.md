# Sub-LLM Calls

## What it is

A **sub-LLM call** is when the model running inside the RLM engine calls *another* LLM (or itself) on a specific piece of text. It's the "recursive" in Recursive Language Model.

## How it works in code

Inside the REPL sandbox, there's a special function available:

```python
result = llm_query(text, question)
```

- `text` — a piece of the document (e.g., a specific chapter, a subset of rows)
- `question` — what to ask about that piece
- `result` — the sub-model's answer, stored as a **Python variable**

## The critical design rule: results are variables, not context

This is the single most important architectural decision in the RLM design, and it's easy to get wrong.

### ❌ Wrong way: inject result into parent's context

```
Parent model's prompt:
  "Here is the document... [100K words]"
  "Here is what sub-model said about section 3: [5K words]"
  "Here is what sub-model said about section 7: [3K words]"
  "Now answer the question..."
```

Each sub-call result makes the parent's context longer → context rot gets worse → you've just recreated the problem you were trying to solve.

### ✅ Right way: result stays as a REPL variable

```python
section3_summary = llm_query(section3, "Summarize the key financial figures")
section7_summary = llm_query(section7, "Summarize the key financial figures")

# Parent model ONLY sees these when it explicitly prints them
print(f"Section 3: {section3_summary}")
print(f"Section 7: {section7_summary}")
```

The parent model's context window stays the same size. It only sees sub-call results when it *chooses* to print them, and even then only the output text — not the full sub-prompt.

## Why recursion is useful

Consider this question over a 500-page document:
> "Across all 12 chapters, which chapter has the highest total spending, and what was the single largest expense in that chapter?"

This requires two levels of work:
1. **Per chapter:** Calculate total spending (need to read each chapter)
2. **Across chapters:** Compare totals, then drill into the winner

With depth-1 recursion:
```python
# Parent model writes:
totals = {}
for i in range(12):
    chapter = corpus.split("CHAPTER")[i+1]
    total = llm_query(chapter, "What is the total spending mentioned? Return only the number.")
    totals[f"Chapter {i+1}"] = float(total)

winner = max(totals, key=totals.get)
print(f"Highest spending: {winner} with ${totals[winner]}")
```

Each `llm_query()` call gives a chapter to a sub-model that can focus on just that chapter — no context rot because each sub-call only sees ~40 pages, not 500.

## Depth-1 vs Depth-2

**Depth-1:** The parent can call sub-models, but the sub-models cannot call further sub-models. One level of delegation.

**Depth-2:** The sub-models CAN also call their own sub-models. Two levels of delegation. So the parent calls a sub-model, and that sub-model can call yet another sub-model.

```
Depth-0:  Model → Answer
                               (no sub-calls at all)

Depth-1:  Model → Sub-call → Answer
                               (one level)

Depth-2:  Model → Sub-call → Sub-sub-call → Answer
                               (two levels)
```

## Why deeper isn't always better

The reproduction paper found that depth-2 causes problems:
- **Format collapse:** The sub-sub-model gets confused about its role and emits raw code instead of answers
- **Latency blowup:** 3.6 seconds → 344.5 seconds on the same query
- **Performative reasoning:** The model starts generating endless, redundant sub-calls instead of converging on an answer

This is the "don't overthink" finding — depth-1 helps, depth-2 hurts.

## Who can be the sub-model?

The sub-model doesn't have to be the same model as the parent. Options:

| Sub-model | Trade-off |
|-----------|-----------|
| Same model | Strongest reasoning, but expensive and slow |
| Smaller model | Cheaper and faster, but may miss nuance |
| Different provider | Can mix local (Ollama) with cloud (Groq) |

In our project, during development we use local Ollama `qwen3:1.7b` for both parent and sub-calls. During real benchmark runs, we use Groq's models (Kimi K2, Llama 3.3 70B) for the parent and potentially a cheaper model for sub-calls.
