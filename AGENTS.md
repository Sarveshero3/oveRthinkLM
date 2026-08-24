# AGENTS.md — oveRthinkLM

## Agent skills

### Issue tracker

Issues are tracked in GitHub Issues via `gh` CLI for `Sarveshero3/oveRthinkLM`. See `docs/agents/issue-tracker.md`.

### Triage labels

Uses canonical label strings (`needs-triage`, `needs-info`, `ready-for-agent`, `ready-for-human`, `wontfix`). See `docs/agents/triage-labels.md`.

### Domain docs

Single-context layout (`CONTEXT.md` + `docs/adr/` at repo root). See `docs/agents/domain.md`.

## Core Project Behavioral Rules

- **From-Scratch Implementation**: The RLM engine, sandbox REPL, sub-LLM caller, and SRLM uncertainty selection are built from scratch. Never import from reference repositories (`alexzhang13/rlm`, `drbillwang/rlm-reproduction`).
- **Sandbox Security Boundary**: The sandbox REPL is an isolated execution environment (subprocess/container with strict timeout/memory limits). Treat all model-generated code as untrusted.
- **Context Isolation**: Recursive sub-call outputs return strictly as isolated REPL variables, avoiding prompt bloat or context rot in parent LLMs.
- **Six-Configuration Matrix**: Benchmark runner must support Depth-0, Depth-1, Depth-2, SRLM, Hybrid-1, and Hybrid-2.
- **Three-Tier LLM Architecture**: 
  - Tier 1: Local Ollama (`qwen3:1.7b` on RTX 3050) for local engine wiring and unit tests.
  - Tier 2: Groq developer tier (Kimi K2, Llama 3.3 70B, GPT-OSS-120B) for high-speed benchmark runs with fast LPU throughput.
  - Tier 3: Together.ai for DeepSeek v3.2 parity.
- **Honest Evaluation**: All 6 configurations must be evaluated and reported with real accuracy, latency, and cost data.
- **DevOps Staging**: Verify local multi-config benchmarks before wiring Jenkins CI/CD.
- **Kubernetes Syntax**: All deployment manifests use real K8s API syntax and run via `podman play kube`.
