# Configuration 6: Hybrid-2 (Depth-2 Recursion + Multi-Level Uncertainty Gating)

## What it is — NOVEL CONTRIBUTION
Combines nested Depth-2 recursion with uncertainty signals evaluated at each recursion boundary.

## Core Research Question
**Can uncertainty signals prevent the format collapse and latency blowup of Depth-2 RLM?**
In Depth-2 RLM, nested sub-calls frequently drift into format collapse or infinite loops. Hybrid-2 introduces uncertainty checks at the recursion boundary to prune unpromising or degenerate branches before they explode the call tree.
