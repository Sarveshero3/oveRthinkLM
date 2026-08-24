# Project Rules & Invariants — oveRthinkLM

These behavioral constraints are established up front and must be strictly adhered to across all phases:

1. **Engine Built From Scratch**: The RLM engine, sandbox loop, sub-call protocol, and SRLM uncertainty mechanisms are built completely from scratch. `github.com/alexzhang13/rlm` and `github.com/drbillwang/rlm-reproduction` are design references and correctness checks only — never add them as project dependencies or import from them. SRLM has no public codebase and must be derived purely from the Apple Research paper.
2. **True Sandbox Isolation**: The REPL sandbox is a real security boundary (subprocess/container level with memory, CPU, and timeout limits), not a restricted `exec()` call or `try/except` wrapper. Model-generated code is treated as actively untrusted.
3. **Variable-Isolated Sub-Calls**: Recursive sub-LLM call results return strictly as REPL variables, never auto-injected into the parent's context window.
4. **Zero Mock Fallbacks in Benchmarks**: No mock or fake data fallbacks in the benchmark runner or scoring logic. All six configurations must execute against real task inputs.
5. **Configurable Three-Tier Model Binding**: Every model choice per role (Tier 1: Local Ollama `qwen3:1.7b` on RTX 3050; Tier 2: Groq developer tier for fast LPU runs on Kimi K2 / Llama 3.3; Tier 3: Together.ai for DeepSeek v3.2 parity) stays behind a configuration value / environment variable, never hardcoded.
6. **Staged DevOps Progression**: Do not wire up the Jenkins CI/CD pipeline until the six-way comparison runs cleanly by hand locally.
7. **Honest Multi-Dimensional Reporting**: Every eval run reports real numbers for all six configurations (Depth-0, Depth-1, Depth-2, SRLM, Hybrid-1, Hybrid-2) across accuracy, latency, and token cost — including configurations that perform worse. The two novel hybrid configurations must be analyzed honestly to show whether recursion and reflection stack, cancel out, or dominate.
8. **Kubernetes-Syntax Orchestration**: All Kubernetes YAML manifests (`deploy/k8s/*.yaml`) adhere to authentic Kubernetes API syntax (`apps/v1`, `v1`) and execute locally via `podman play kube` to satisfy the ENSP461 capstone requirement.
