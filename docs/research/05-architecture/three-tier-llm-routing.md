# Three-Tier LLM Routing Architecture

| Tier | Provider | Primary Models | Role & Justification |
|---|---|---|---|
| **Tier 1** | Local Ollama (`D:\OllamaModels`) | `qwen3:1.7b` (RTX 3050) | Local engine wiring, REPL loop unit testing, offline smoke tests without API costs. |
| **Tier 2** | Groq Developer Tier | `Kimi K2`, `Llama 3.3 70B`, `GPT-OSS-120B` | Primary benchmark backend. High-speed LPU throughput prevents combinatorial latency blowup across recursive call trees. `Kimi K2` provides direct parity with the Wang 2026 reproduction study. |
| **Tier 3** | Together.ai | `DeepSeek v3.2` | Fallback for exact DeepSeek v3.2 architectural parity (Groq serves a distilled variant). |
| **Tier 4 (Last Resort)** | Anthropic / OpenAI | `Claude 3.5 Sonnet`, `GPT-4o` | Reserved for high-complexity gold standard evaluations if open-weight models display severe format collapse. |
