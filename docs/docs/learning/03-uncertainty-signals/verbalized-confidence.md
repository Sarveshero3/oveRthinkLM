# Verbalized Confidence (Uncertainty Signal #2)

## The idea

Simply ask the model: "How confident are you in this answer?"

LLMs can often tell you when they're uncertain. This is called **verbalized** or **elicited** confidence — the model explicitly states its confidence level.

## How it works

After the model generates an answer, we add a follow-up prompt:

```
Your answer was: "There were 4 board meetings in Q3."

On a scale of 0 to 100, how confident are you in this answer? 
Consider:
- Did you find clear, unambiguous evidence?
- Are there alternative interpretations?
- Did you have to make any assumptions?

Respond with only a number.
```

The model might respond: `85`

## Why it works (sometimes)

Models have been trained on millions of examples where humans express uncertainty. When the evidence is clear, the model tends to say high confidence. When it had to guess or extrapolate, it tends to say lower confidence.

## Why it's imperfect

- **Overconfidence:** Models often say "95" when they should say "60" — they're biased toward high confidence
- **Calibration varies by model:** Some models are better calibrated than others
- **Not independently reliable:** Works best when combined with the other two signals, not alone

## The metric

```
Verbalized Confidence Score = (model's stated confidence) / 100
```

Simple normalized value between 0.0 and 1.0.

## In our project

We extract this as part of the SRLM and Hybrid configurations. Each candidate program's answer gets a verbalized confidence score. A program where the model says "95" for every answer is ranked higher than one where it says "40".
