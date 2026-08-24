# Configuration 1: Depth-0 Baseline (Vanilla LLM)

## What it is
The standard way people interact with LLMs today. The prompt contains the entire context/document plus the user query.

```
+--------------------------------------------------------+
¦ Context Document (e.g. 50,000 tokens) + User Question  ¦
+--------------------------------------------------------+
                           ¦ Direct API Call
                           ?
                    +--------------+
                    ¦ Standard LLM ¦
                    +--------------+
                           ¦
                           ?
                     Final Answer
```

## Characteristics
- **Scaffolding**: None (No Python REPL, no code execution, no sub-calls).
- **Inference Calls**: Exactly 1 call.
- **Latency**: Fast (depends only on output token length and TTFT).
- **Cost**: Linear in total context length (all input tokens billed in single prompt).

## Expected Behavior & Research Hypothesis
- **Simple Retrieval (Needle in Haystack)**: High accuracy on frontier models that support long context.
- **Complex Multi-Hop Reasoning**: High failure rate due to **context rot** (attention dispersion across long token spans).
