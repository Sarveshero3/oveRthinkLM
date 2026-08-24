# How the Three Uncertainty Signals Combine

## The three signals recap

| Signal | What it measures | How | Cost |
|--------|-----------------|-----|------|
| **Self-Consistency** | Statistical agreement | Run N times, count matches | High (N extra calls) |
| **Verbalized Confidence** | Model's self-assessment | Ask "how confident?" | Low (1 extra call) |
| **Reasoning Length** | Behavioral hedging | Count answer tokens | Free (already have the answer) |

## Combining into a composite score

Apple's SRLM paper uses a weighted combination. The simplest version:

```
composite_score = w1 × self_consistency + w2 × verbalized_confidence + w3 × reasoning_length_score
```

Where `w1 + w2 + w3 = 1` and all scores are normalized to [0, 1].

The paper found that self-consistency is the most reliable signal, so it typically gets the highest weight.

## How SRLM uses the composite score

```
Given a question and a document:

1. Generate 5 candidate exploration programs (different strategies)
2. Execute each program → get 5 candidate answers
3. For each candidate:
   a. Run it 3 more times → self-consistency score
   b. Ask model "how confident?" → verbalized confidence score
   c. Count answer tokens → reasoning length score
   d. composite = weighted combination
4. Pick the candidate with the highest composite score
5. Return that as the final answer
```

## How the Hybrids would use it (the design question)

This is where our project gets novel. SRLM applies these signals to *flat programs* (no recursion). Our hybrids apply them to *programs that contain recursive sub-calls*.

The question is: WHERE in the recursive process do the signals get applied?

### Option A: Program selection (before anything runs)

Generate N candidate programs (some of which include `llm_query()` sub-calls), score them by uncertainty signals, run only the best one.

```
Generate 5 programs → Score all 5 → Pick best → Execute (with recursion if chosen)
```

This is SRLM's approach applied to programs that happen to contain recursion.

### Option B: Sub-call gating (during execution)

Let the program run, but when it's about to make a recursive `llm_query()` call, pause and ask: "Is this sub-call likely to help? Or should we just answer with what we have?"

```
Program runs → about to call llm_query() → Score whether to proceed → Continue or answer directly
```

This is a recursion-pruning mechanism. It might prevent depth-2's "performative reasoning" loops.

### Option C: Result arbitration (after execution)

Let multiple recursive programs run to completion, then use uncertainty signals to pick the best result.

```
Run 5 programs (all with recursion) → Get 5 answers → Score answers → Pick best
```

This is the most expensive but also the most thorough.

## Why this is an important design decision

The choice between A, B, and C changes:
- **Cost:** A is cheapest (only score programs, not sub-calls). C is most expensive (run everything).
- **Novelty:** B is the most architecturally novel — nobody has done recursion gating with uncertainty signals.
- **Comparison fairness:** A is the fairest comparison to SRLM because it's the same mechanism applied to a richer program space.
- **Format collapse mitigation:** B is the most likely to prevent depth-2's problems, because it can short-circuit bad sub-call chains.

This is exactly the design question that was asked in the grill interview.
