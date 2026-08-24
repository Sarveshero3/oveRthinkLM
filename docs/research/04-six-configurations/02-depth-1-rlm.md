# Configuration 2: Depth-1 RLM (Single-Level Recursion)

## What it is
The model interacts with a Python REPL holding the document in variable `corpus`. It writes Python code to slice, regex-search, and make recursive sub-LLM calls (`llm_query(slice, sub_question)`).
Crucially, **sub-calls cannot make further sub-calls** (recursion depth is clamped at 1).

```
+--------------------------------------------------------+
¦ RLM Engine: Prompt with variable metadata & Python REPL¦
+--------------------------------------------------------+
                           ¦ Writes exploration script
                           ?
                  +------------------+
                  ¦   Sandbox REPL   ¦?--------+
                  ¦ (corpus="...")   ¦         ¦
                  +------------------+         ¦ Sub-call output assigned
                           ¦ llm_query(slice)  ¦ to Python variable
                           ?                   ¦ (not injected into parent)
                  +------------------+         ¦
                  ¦ Sub-LLM Instance +---------+
                  ¦ (Depth = 1 max)  ¦
                  +------------------+
```

## Characteristics
- **Context Management**: Context offloaded to REPL memory; parent LLM prompt stays compact.
- **Isolation**: Sub-call responses return strictly as variables in Python memory (`res = llm_query(...)`), avoiding context pollution in parent prompt.
- **Inference Calls**: 1 root call + $k$ sub-calls ($k \ge 0$).

## Expected Behavior & Research Hypothesis
- **Complex Multi-Hop Reasoning**: High accuracy boost (breaks massive documents into focused, parallelizable sub-queries).
- **Simple Retrieval**: Paradoxical performance drop or neutral compared to Depth-0 due to programmatic overhead on trivial lookups ("Think, But Don't Overthink" finding).
