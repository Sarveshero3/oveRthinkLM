# Design Decision: Hybrid Uncertainty Integration Points

## The Core Question
In **Hybrid-1** and **Hybrid-2**, how and where should the SRLM uncertainty signals (self-consistency, verbalized confidence, reasoning length) intervene in the recursive RLM loop?

## Architectural Options

### Option A: Pre-Execution Program Selection (Recommended)
- **Mechanism**: The model generates $N$ candidate exploration programs (which may include `llm_query` recursive calls). Uncertainty signals score the candidates *before* execution; only the highest-scoring candidate program is executed.
- **Pros**: Cleanest ablation comparison against pure SRLM; limits cost and branching explosion.
- **Cons**: Does not dynamically prune sub-calls midway through execution.

### Option B: Mid-Execution Sub-Call Gating
- **Mechanism**: The program executes normally, but before firing any `llm_query()` sub-call, the engine computes uncertainty on the current partial answer. If confidence is already high, the sub-call is pruned.
- **Pros**: Directly attacks "performative reasoning" and reduces unnecessary recursive calls.
- **Cons**: Requires pausing program execution state; higher orchestration complexity.

### Option C: Post-Execution Result Arbitration
- **Mechanism**: Multiple complete recursive branches are executed in parallel, and uncertainty signals select among the final candidate answers.
- **Pros**: Maximum answer quality through parallel search.
- **Cons**: Extreme cost and latency multiplication ($N \times O(b^d)$).
