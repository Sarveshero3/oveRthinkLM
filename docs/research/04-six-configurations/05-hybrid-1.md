# Configuration 5: Hybrid-1 (Depth-1 Recursion + Uncertainty Search)

## What it is — NOVEL CONTRIBUTION
A hybrid architecture that merges Depth-1 recursion with SRLM uncertainty signals.

Instead of executing arbitrary recursive programs blindly, the engine generates candidate recursive exploration programs (which may include `llm_query` invocations) and uses uncertainty scoring to guide program selection and execution.

## Core Research Question
**Do recursion gains and reflection gains stack, cancel out, or does one dominate?**
- If *stack*: Hybrid-1 achieves higher accuracy than both Depth-1 RLM and SRLM independently.
- If *cancel out*: The uncertainty search prunes away the benefits of recursion or adds redundant latency.
