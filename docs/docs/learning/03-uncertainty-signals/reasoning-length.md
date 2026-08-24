# Reasoning Length (Uncertainty Signal #3)

## The idea

When a model is confident, it gives short, direct answers. When it's uncertain, it hedges, qualifies, and explains at length. Shorter reasoning = higher confidence.

## Example

**Confident answer (short):**
> "The total revenue was $4.2 billion."

**Uncertain answer (long):**
> "Based on the available information, it appears that the total revenue figure might be approximately $4.2 billion, though this could also include the subsidiary's revenue which was reported separately in section 7.3, and there may be some overlap with the figures mentioned in the consolidated statement on page 45, so the actual number could be anywhere between $3.8 billion and $4.5 billion depending on interpretation..."

The second answer is longer *because* the model isn't sure.

## The metric

```
Reasoning Length Score = 1 / (1 + log(token_count))
```

Or simpler: just use the inverse of token count, normalized.

- Short answer (20 tokens) → high score
- Long answer (500 tokens) → low score

## Why this is counterintuitive

You might think "longer = more thorough = better." But empirically, for factual questions with definitive answers, the opposite is true. The length isn't depth of analysis — it's hedging.

This is a **behavioral** uncertainty signal — we're measuring the model's *behavior* (how much it writes) rather than asking it directly (verbalized) or testing it statistically (self-consistency).

## Limitations

- Doesn't work for questions that genuinely require long answers (e.g., "Summarize all 12 chapters")
- Works best for factual/numerical questions with short expected answers
- Needs to be calibrated per task type

## In our project

We use this as the third component of the uncertainty triplet. It's the cheapest signal to compute — no extra API calls needed, just count the tokens of the answer that was already generated.
