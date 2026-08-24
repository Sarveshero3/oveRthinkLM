# overthink — PRD

## 0. College capstone requirement (verbatim, ENSP461)

> Develop one complete end-to-end DevOps automation platform that integrates version control, a CI/CD pipeline, containerization, Kubernetes orchestration, infrastructure automation, monitoring, logging, security, and an advanced deployment strategy for a chosen application. The platform should automate the full software delivery lifecycle — from code commit to production deployment — with observability, security, and recoverability built in, so that the workflow is reproducible and production-ready. (120 marks)

**On "Kubernetes orchestration":** same resolution as before, carried over because it's a fact about the course, not the project. This uses Podman, not a K8s distro. Every service is defined with real Kubernetes-syntax YAML (Deployment/Pod/Service manifests) and run with `podman play kube`, not `kubectl apply` against a cluster. State this explicitly in the report.

## 1. Problem statement

Frontier LLMs suffer "context rot" — output quality degrades well before hitting the model's stated context limit, even as context windows grow into the millions of tokens. Recursive Language Models (RLMs), proposed by Zhang, Kraska, and Khattab (MIT CSAIL, arXiv:2512.24601), treat a long prompt as an external environment: the model gets a Python REPL, writes code to programmatically slice and explore the input, and recursively calls itself (or smaller sub-models) on pieces of it, rather than reading everything directly. Sub-call results return as REPL variables, not auto-injected context.

The literature disagrees on why this works, and that disagreement is the actual subject of this project. "Think, But Don't Overthink: Reproducing Recursive Language Models" (arXiv:2603.02615, March 2026) found the failure mode is two-sided, not just "deeper is worse": depth-1 RLMs dramatically help complex reasoning tasks but paradoxically underperform a vanilla LLM on simple retrieval queries, and depth-2 goes further, causing format collapse with latency observed climbing from roughly 3.6 seconds to 344.5 seconds on the same query. "Recursive Language Models Meet Uncertainty" (arXiv:2603.15653, March 2026 — Apple Research) found recursion depth isn't even the primary driver of RLM's gains at all — a simpler self-reflective program search (SRLM), using self-consistency, reasoning length, and verbalized confidence as uncertainty signals, can match or beat naive recursion without recursing deeper. This project builds a working RLM engine and empirically tests where these claims hold, using it as an honest data point rather than assuming either paper is right.

## 2. Goals

- Build a working RLM engine **from scratch** — your own REPL sandbox, your own recursion control loop, your own sub-LLM call protocol. Two reference implementations exist and are design reference and correctness checks only, never dependencies the project imports: `github.com/alexzhang13/rlm` (the original paper's code) and `github.com/drbillwang/rlm-reproduction` (the "Think, But Don't Overthink" reproduction). SRLM (Apple's paper) has no public code at all — that piece has zero reference to lean on and must be understood from the paper alone. The learning value and the research credibility both depend on this being genuinely understood, not wired together from someone else's library.
- Build a benchmark runner that compares six configurations on the same task set: depth-0 (plain LLM, no scaffold), depth-1 RLM, depth-2 RLM, SRLM (self-reflection only, no recursion), and two novel hybrids — **Hybrid-1** (depth-1 recursion plus SRLM's uncertainty signals applied at that level) and **Hybrid-2** (depth-2 recursion plus the same signals applied at each level). The two hybrids are the project's actual novel contribution — no published work combines recursive sub-calls with uncertainty-aware self-reflection, confirmed by search as of August 2026.
- The task set must include both complex-reasoning items and simple-retrieval items, not just complex ones — the depth-1-hurts-simple-retrieval finding above is only observable if both are present.
- Produce a real, honestly-reported comparison — accuracy, cost, and latency per configuration — not just a working demo. This project may become a research paper; treat every result, including ones that make the hybrids look bad, as reportable.
- Deploy the full pipeline with real DevOps rigor: containers, K8s-syntax orchestration via Podman, CI/CD, monitoring, security, advanced deployment.

## 3. Non-goals

- Not post-training a model to be natively RLM-aware — the original paper's fine-tuning experiment is out of scope for a semester on an RTX 3050.
- Not claiming to resolve the recursion-helps-or-hurts debate definitively. A solo capstone's benchmark runs are a genuine data point, not the final word — say so in the write-up rather than overclaiming.
- Not a general-purpose coding agent. The REPL is scoped to context-exploration operations (slicing, searching, transforming the input, spawning sub-calls), not arbitrary development tasks.

## 4. Architecture

| Component | Role |
|---|---|
| **RLM engine** | Orchestrates the loop: given a long document and a query, decides whether to answer directly, write exploratory code, or recurse. |
| **Sandbox REPL** | Isolated Python execution environment where the engine's generated code actually runs. This is the real security boundary — untrusted, model-generated code executing on real input. |
| **Sub-LLM caller** | Handles recursive calls to a smaller or cheaper model. Results return as REPL variables, never auto-injected into the parent's context, matching the actual RLM design. |
| **Benchmark runner** | Runs the same query set across all six configurations against a long-context task set. |
| **Trajectory dashboard** | Visualizes the recursive call tree per run: which REPL commands executed, which sub-calls fired, cost and latency per branch, final accuracy per configuration. |
| **Jenkins continuous benchmarking** | Reruns the benchmark suite on every code change and flags whether a change helped or hurt the actual research metric, not just whether the build passed. |

## 5. Task set

Full OOLONG or S-NIAH (the benchmarks the original papers use) may be too large to run repeatedly on local hardware within a semester. Antigravity should propose a scoped-down task set during the techspec phase — a smaller number of long documents with verifiable answers, enough diversity to be meaningful, small enough to rerun on every Jenkins build. Must include both complex-reasoning and simple-retrieval items per section 2. This is a real design decision, not a detail to skip past.

## 6. Success criteria

- Engine runs end to end on all six configurations without manual intervention.
- Benchmark comparison produces real numbers — accuracy, cost, latency — not just "it ran."
- The comparison actually surfaces (or actually fails to reproduce) the two-sided depth-1 effect and the SRLM-vs-recursion question, not just a single aggregate accuracy number per configuration.
- The two hybrid configurations show whether recursion's gains and self-reflection's gains stack, cancel out, or one dominates — that comparison is the actual point, not just "hybrid beat baseline."
- Trajectory dashboard shows an actual recursive call tree, not a flat log.
- Full pipeline deployed via Podman pods, real K8s-syntax manifests via `podman play kube`, Jenkins CI/CD.
- Final write-up states clearly where this project's findings agree or disagree with the two follow-up papers, and why.

## 7. Tech stack

- **Engine and services**: Python, FastAPI per service
- **Sandbox**: isolated Python execution (subprocess/container-level isolation, not just a restricted `exec()` — a real security boundary, not a fig leaf)
- **LLM backend**: hybrid, three tiers, per `machine-environment.md`. Local Ollama (`qwen3:1.7b`, GPU-accelerated on the RTX 3050) for wiring up and debugging the engine itself, where model quality doesn't matter yet. **Groq** (free developer tier, no credit card, OpenAI-compatible SDK) for the real benchmark runs needing a capable model at real speed — it hosts Kimi K2, one of the two models the reproduction paper used, plus Llama 3.3 70B and GPT-OSS-120B as additional comparison points, and its LPU speed matters a lot given six configurations times multiple trials times recursive sub-calls compounding total call count. **Together.ai** as the fallback specifically for DeepSeek v3.2 parity with the reproduction paper, since Groq's DeepSeek offering is a distilled variant, not the same model — Together carries the closer match. Keep the paid Claude/GPT API as the option of last resort for anything needing genuinely frontier-level reasoning beyond what the open-weight models on Groq/Together provide.
- **Containers**: Podman, one pod per component (engine, sandbox, sub-LLM caller, benchmark runner, dashboard). Podman machine lives at `D:\WSL\podman-machine-default` — see `machine-environment.md`.
- **CI/CD**: Jenkins — test, build, deploy, and rerun the benchmark suite, reporting regressions in accuracy/cost alongside build status.
- **Observability**: Prometheus/Grafana for recursion depth distribution, cost per query, sandbox resource usage; the trajectory dashboard is a separate, purpose-built view for the recursive call tree itself.

## 8. Phases

1. **Reproduce the mechanism, no containers** — get the base RLM loop working locally against one toy long document. Confirm the REPL-plus-recursion approach actually functions before building anything around it.
2. **Build the four-way comparison** — depth-0, depth-1, depth-2, self-reflect-only, against the scoped task set from section 5.
3. **Containerize** — Podman pods, K8s-syntax manifests, `podman play kube`.
4. **Jenkins + continuous benchmarking** — wired up after step 2 and 3 work locally, not before.
5. **Dashboard and write-up** — trajectory visualization, then the honest comparison against the two follow-up papers' claims.

## 9. Known risks

- Recursion is inherently high-variance — the original paper notes cost stays comparable to a single call on average but varies a lot, since the model can keep recursing or iterating. Expect to need multiple trials per configuration for a stable signal, which costs real time even though no training is involved.
- **Set an explicit cloud API budget before running the full benchmark, not after.** Four configurations x multiple trials x a task set with both complex and simple items, run against a cloud API for the depth-0 baseline and higher-fidelity comparisons, adds up fast — especially once depth-2's latency and token-cost blowup (the 3.6s-to-344.5s pattern from the reproduction study) shows up in your own runs too. Decide the cap up front and design the task set size around it, rather than discovering the cost mid-run.
- A small local model (`qwen3:1.7b`) will not necessarily reproduce the same overthinking/self-reflection dynamics the papers found on frontier models (GPT-5, DeepSeek v3.2, Kimi K2). Results on a small local model are a different, still-legitimate experiment — say so explicitly rather than implying a direct reproduction.
- The sandbox is a real security boundary, not a formality — the same lesson from the trust-layer project applies here: an isolation claim that isn't actually load-bearing is worse than not claiming it. Don't let "sandboxed" mean "wrapped in a try/except."
- This is a research-flavored capstone. The bar is an honest, well-instrumented comparison, not a definitive answer to an open debate.

## 10. Repo

Live at **github.com/Sarveshero3/oveRthinkLM**. The existing `corrobor8` repo's Lab 1 Git-workflow exercise (init, branch, merge, push) already served its purpose for that lab's grading and doesn't need to be touched — this is a clean pivot, not a loss of prior work.
