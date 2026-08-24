# oveRthinkLM

An empirical evaluation platform and DevOps automation pipeline testing **Recursive Language Models (RLMs)**, **Self-Reflective Program Search (SRLM)**, and **Novel Hybrid Architectures** across accuracy, latency, and token cost under context rot.

## Language

**Recursive Language Model (RLM)**:
An inference architecture where the model treats long context as an external variable within a code execution environment (REPL) and writes Python code to slice, inspect, and recursively call sub-models on subsets of the data.
_Avoid_: Agent loop, recursive agent, code agent

**Sandbox REPL**:
The isolated execution environment with strict resource and capability boundaries where model-generated exploration code is executed.
_Avoid_: Code runner, executor, interpreter

**Sub-LLM Call**:
A programmatic invocation of an LLM initiated from within the REPL environment whose output is assigned to a Python variable rather than appended to the caller's prompt context.
_Avoid_: Tool call, child agent, delegated prompt

**Recursion Depth**:
The maximum nesting level of recursive sub-LLM calls permitted during execution (Depth-0 = vanilla direct prompt, Depth-1 = single-level sub-calls, Depth-2 = nested sub-calls within sub-calls).
_Avoid_: Nesting level, call stack depth, recursion tier

**Self-Reflective Program Search (SRLM)**:
A non-recursive long-context technique (Apple Research, arXiv:2603.15653) that generates candidate context-interaction programs and selects solutions using uncertainty signals without recursive sub-queries.
_Avoid_: Reflection loop, self-correction, iterative prompting

**Hybrid-1**:
A novel architecture combining Depth-1 recursive sub-calls with SRLM's uncertainty signals applied at the sub-call selection boundary to evaluate if recursion and reflection stack or compete.
_Avoid_: Augmented RLM, depth-1 reflection

**Hybrid-2**:
A novel architecture combining Depth-2 nested recursion with multi-level uncertainty signals applied at each recursion boundary to investigate format collapse mitigation.
_Avoid_: Deep reflection, nested hybrid

**Uncertainty Signals**:
Intrinsic metric triplets used by SRLM and Hybrid configurations to score candidate programs:
1. **Self-Consistency**: Empirical agreement across sampled execution trajectories.
2. **Verbalized Confidence**: The model's explicit semantic confidence rating.
3. **Reasoning Length**: Inverse behavioral uncertainty proxy (shorter concise traces indicating higher certainty).
_Avoid_: Confidence score, heuristics, quality metrics

**Context Rot**:
The empirical degradation in LLM comprehension and retrieval performance as input context length increases, occurring well before theoretical context window limits are reached.
_Avoid_: Attention decay, context loss, haystack degradation

**Format Collapse**:
The observed failure mode where an LLM under recursive pressure loses its structural output fidelity (e.g. emitting raw code or unfinished tokens instead of answers).
_Avoid_: Syntax error, parse failure, hallucination

**Trajectory**:
The complete structured record of all REPL interactions, code executions, sub-LLM calls, token costs, and latencies across the execution tree for a given query.
_Avoid_: Execution log, trace, call history
