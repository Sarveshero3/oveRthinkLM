# Recursion Depth

## The concept

**Recursion depth** is the maximum number of nested levels of sub-LLM calls the engine permits. It's the single most debated parameter in the RLM literature.

## The six depths/configurations we test

| Config | Recursion? | Reflection? | What it does |
|--------|-----------|-------------|--------------|
| **Depth-0** | ❌ None | ❌ None | Plain LLM. Paste the document into the prompt, ask the question, get an answer. No REPL, no code, no sub-calls. This is the baseline. |
| **Depth-1** | ✅ 1 level | ❌ None | RLM with one level of sub-calls. The model can write code and call `llm_query()`, but the sub-model cannot make its own sub-calls. |
| **Depth-2** | ✅ 2 levels | ❌ None | RLM with nested sub-calls. The sub-model can also call `llm_query()`, creating a tree of calls. Known to cause format collapse and latency blowup. |
| **SRLM** | ❌ None | ✅ Yes | No recursion at all. Instead, generates multiple candidate exploration programs and picks the best one using uncertainty signals. Apple's approach. |
| **Hybrid-1** | ✅ 1 level | ✅ Yes | OUR NOVEL IDEA: Depth-1 recursion combined with SRLM's uncertainty signals. Does combining them help or hurt? |
| **Hybrid-2** | ✅ 2 levels | ✅ Yes | OUR NOVEL IDEA: Depth-2 recursion combined with uncertainty signals at each level. Can uncertainty signals prevent the format collapse that depth-2 normally causes? |

## Why depth matters

### The optimistic story (original RLM paper)
More depth = more ability to decompose complex problems. A depth-2 RLM can break a problem into sub-problems, then break *those* into sub-sub-problems. Theoretically more powerful.

### The pessimistic story (reproduction paper)
More depth = more chances for things to go wrong:
- The model loses track of what format it should output in (**format collapse**)
- Each recursive call adds latency, and the calls compound (**latency blowup**: 3.6s → 344.5s)
- The model starts generating busywork sub-calls that don't contribute to the answer (**performative reasoning**)
- Simple questions that a plain LLM answers correctly get *worse* with recursion (**overthinking simple tasks**)

### The alternative story (Apple SRLM)
Depth doesn't even matter — what matters is *choosing the right exploration strategy*, which you can do without recursion. Generate several candidate approaches, measure which one the model is most confident about, pick that one.

## What our project investigates

The six configurations form a clean comparison grid:

```
                    No Reflection    With Reflection (SRLM)
                    ─────────────    ──────────────────────
No Recursion:       Depth-0          SRLM
1-level Recursion:  Depth-1          Hybrid-1  ← novel
2-level Recursion:  Depth-2          Hybrid-2  ← novel
```

This grid lets us answer:
1. **Does recursion help?** Compare Depth-0 vs Depth-1 vs Depth-2 (left column)
2. **Does reflection help?** Compare left column vs right column at each depth
3. **Do they stack?** Is Hybrid-1 better than both Depth-1 and SRLM alone?
4. **Can reflection fix depth-2's problems?** Does Hybrid-2 avoid the format collapse and latency blowup that Depth-2 suffers?

Nobody has published answers to questions 3 and 4. That's the novel contribution.
