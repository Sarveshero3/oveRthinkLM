# Self-Consistency (Uncertainty Signal #1)

## The idea

Run the same program multiple times with slight randomness. If the answer is the same every time, the model is confident. If it varies, the model is guessing.

## How it works

LLMs have a parameter called **temperature** that controls randomness:
- Temperature 0 = always pick the most likely next token (deterministic)
- Temperature 0.7 = sometimes pick less likely tokens (some randomness)
- Temperature 1.0+ = very random

Self-consistency uses temperature > 0 deliberately:

```
Question: "How many board meetings in Q3?"

Run 1 (temp=0.7): "4 meetings"
Run 2 (temp=0.7): "4 meetings"  
Run 3 (temp=0.7): "4 meetings"
Run 4 (temp=0.7): "4 meetings"
Run 5 (temp=0.7): "4 meetings"
→ Self-consistency: 5/5 = 100% — very confident
```

vs:

```
Question: "What was the main theme of the CEO's letter?"

Run 1 (temp=0.7): "Growth and innovation"
Run 2 (temp=0.7): "Digital transformation"
Run 3 (temp=0.7): "Sustainability and growth"
Run 4 (temp=0.7): "Innovation-driven growth"
Run 5 (temp=0.7): "Growth and innovation"
→ Self-consistency: ~40% agreement — uncertain
```

## The metric

```
Self-Consistency Score = (count of most common answer) / (total runs)
```

Score ranges from `1/N` (completely inconsistent) to `1.0` (perfectly consistent).

## Trade-off

More runs = more reliable signal, but also more API calls = more cost. For our project, we need to balance this against the fact that we're already doing 6 configurations × multiple trials × a task set.
