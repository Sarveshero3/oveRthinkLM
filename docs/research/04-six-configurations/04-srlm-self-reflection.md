# Configuration 4: SRLM (Self-Reflective Program Search)

## What it is
The method proposed by Apple Research (arXiv:2603.15653). **Zero recursive sub-calls**.
Instead of recursing, the model generates $N$ candidate Python programs representing diverse exploration hypotheses over `corpus`. Each program executes in the REPL, and the engine evaluates the candidate outputs using three **uncertainty signals**:
1. **Self-Consistency**: Agreement across sampled executions.
2. **Verbalized Confidence**: Model self-reported score.
3. **Reasoning Length**: Conciseness proxy (shorter = more certain).

```
                      +--------------------------+
                      ¦ Generate N Program Seeds ¦
                      +--------------------------+
                                   ¦
          +------------------------+------------------------+
          ?                        ?                        ?
    +-----------+            +-----------+            +-----------+
    ¦ Program A ¦            ¦ Program B ¦            ¦ Program C ¦
    +-----------+            +-----------+            +-----------+
          ?                        ?                        ?
    [Exec REPL]              [Exec REPL]              [Exec REPL]
          ?                        ?                        ?
    [Score U(A)]             [Score U(B)]             [Score U(C)]
          +-------------------------------------------------+
                                   ?
                        ArgMax Composite Score
                                   ?
                              Final Answer
```

## Expected Behavior & Research Hypothesis
- Matches or outperforms Depth-1 RLM on accuracy without the cost/latency variance of recursive tree branching.
