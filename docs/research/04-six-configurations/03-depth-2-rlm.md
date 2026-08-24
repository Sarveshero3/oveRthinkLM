# Configuration 3: Depth-2 RLM (Nested Recursion)

## What it is
The RLM engine allows sub-LLM calls to themselves launch sub-sub-LLM calls up to a maximum nesting depth of 2.

```
Root RLM (Depth 0)
    +-- Sub-LLM Call (Depth 1)
            +-- Sub-Sub-LLM Call (Depth 2 - Leaf)
```

## Characteristics
- **Branching Factor**: If root spawns $b$ sub-calls and each spawns $b$ sub-sub-calls, total LLM invocations scale as $O(b^2)$.
- **Latency Compounding**: Tree execution can compound serial wall-clock time dramatically.

## Expected Failure Modes (Wang 2026 Reproduction)
1. **Format Collapse**: Deeper sub-agents lose prompt framing and emit raw code strings or unparsed thoughts instead of answers.
2. **Parametric Hallucination**: Deeper sub-agents drift from the document context and hallucinate from model weights.
3. **Latency Blowup**: 3.6s $\to$ 344.5s observed in published trials.
