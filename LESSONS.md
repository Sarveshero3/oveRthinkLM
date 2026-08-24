# Lessons Learned — oveRthinkLM

Continuous record of engineering insights, bugs encountered, and architecture realizations.

## Entries

### [2026-08-25 00:05] PRD Expansion: 6-Configuration Comparison & 3-Tier LLM Architecture
- **Research Novelty in Hybrids**: Combining recursion depth with uncertainty signals (`Hybrid-1` and `Hybrid-2`) provides a novel contribution unaddressed in published literature (as of August 2026). Measuring whether recursion and reflection stack or compete requires clean ablation baselines across all 6 configurations.
- **LLM Tiering & Groq LPU Speed**: Recursive call trees compound call count exponentially ($O(b^d)$). Using Groq's high-throughput LPU inference (Kimi K2, Llama 3.3 70B) is critical for preventing combinatorial latency blowup during multi-trial benchmark runs, while preserving local Ollama (`qwen3:1.7b`) for engine wiring and Together.ai for DeepSeek v3.2 parity.
- **SRLM Zero-Reference Grounding**: Unlike RLM which has public reference implementations, Apple's SRLM has no public code. Its uncertainty signals (self-consistency sampling, verbalized confidence extraction, and reasoning length tracking) must be engineered cleanly from first principles.
- **Hardware Realities**: RTX 3050 handles local Ollama lightweight inference with storage routed to `D:\OllamaModels`. Podman machine VM resides on `D:\WSL\podman-machine-default`.
