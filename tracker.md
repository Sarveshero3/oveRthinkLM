# Task Tracker: oveRthinkLM

Track work across all project phases. Updated continually as tasks transition from `[ ] Not Started` to `[-] In Progress` to `[x] Done`.

## Step 1 & 2: Setup & Environment Initialization
- [x] Create and verify `machine-environment.md` and root `PRD.md` for `oveRthinkLM`
- [x] Run `setup-matt-pocock-skills` scaffold (`AGENTS.md`, `CONTEXT.md`, `docs/agents/`, `.agents/skills/`)
- [x] Purge legacy files and initialize persistent governance (`rules.md`, `tracker.md`, `implementation-log.md`, `LESSONS.md`, `README.md`)
- [x] Incorporate 6-configuration benchmark matrix (Depth-0, Depth-1, Depth-2, SRLM, Hybrid-1, Hybrid-2) and 3-tier LLM backends (Ollama, Groq, Together.ai)

## Step 3: Design & Specification (`grill-with-docs`)
- [ ] Deliver Document 1: `techspec.md` (Module layout, REPL sandbox isolation boundary, sub-LLM call protocol, SRLM uncertainty engine, 6-config runner architecture, scoped task set decision)
- [ ] Review & Refine `techspec.md`
- [ ] Deliver Document 2: `systemflow.md` (End-to-end query path: explore vs recurse vs self-reflect vs hybrid branch resolution, trajectory logging)
- [ ] Review & Refine `systemflow.md`
- [ ] Deliver Document 3: `design.md` (Backend component architectures, sandbox security model, Podman pod layout, Trajectory call-tree dashboard UI/UX)
- [ ] Review & Refine `design.md`
- [ ] Deliver Document 4: `schema.md` (Trajectory JSON schemas, benchmark evaluation result models, task dataset schema, uncertainty signal payloads)
- [ ] Review & Refine `schema.md`

## Phase 1: Local Mechanism Reproduction (No Containers)
- [ ] Isolated Python Subprocess REPL Sandbox with timeouts and memory limits
- [ ] Sub-LLM caller protocol (Local Ollama `qwen3:1.7b` & Groq API bindings returning REPL variables)
- [ ] Core RLM exploration and recursion control loop
- [ ] SRLM uncertainty scoring engine (Self-consistency, verbalized confidence, reasoning length)
- [ ] Mechanism validation against single toy long document

## Phase 2: Six-Way Benchmark Comparison Engine
- [ ] Scoped task set dataset generation (Simple Retrieval + Complex Reasoning)
- [ ] Configuration 1: Depth-0 baseline runner (Vanilla LLM direct prompt)
- [ ] Configuration 2: Depth-1 RLM runner
- [ ] Configuration 3: Depth-2 RLM runner (Format collapse & latency blowup tracking)
- [ ] Configuration 4: SRLM runner (Self-reflective program search without recursion)
- [ ] Configuration 5: Hybrid-1 runner (Depth-1 recursion + uncertainty signal filtering)
- [ ] Configuration 6: Hybrid-2 runner (Depth-2 recursion + multi-level uncertainty signal filtering)
- [ ] Automated scoring and comparative metric aggregation (Accuracy, Cost, Latency, Hybrid interaction dynamics)

## Phase 3: Containerization & Podman Orchestration
- [ ] Containerfiles for services (Engine, Sandbox, Sub-LLM Caller, Runner, Dashboard)
- [ ] Kubernetes-syntax YAML manifests (`deploy/k8s/`) for Pods, Services, ConfigMaps
- [ ] Local deployment verification via `podman play kube` on Windows/WSL2 Podman machine

## Phase 4: Jenkins Continuous Benchmarking CI/CD
- [ ] Declarative `Jenkinsfile` (Lint, Unit Tests, Podman Build, Manifest Validation)
- [ ] Continuous benchmarking pipeline stage (Runs benchmark suite and flags research metric regressions)

## Phase 5: Trajectory Dashboard, Observability & Research Paper Write-Up
- [ ] Trajectory call-tree visualizer dashboard (Visualizing recursive trees, sub-calls, and uncertainty scores)
- [ ] Prometheus metrics & Grafana dashboard (Recursion depth distribution, sandbox resources, cost/latency)
- [ ] Final research evaluation write-up (Empirical findings vs MIT RLM, Wang reproduction, Apple SRLM, and Novel Hybrid insights)
- [ ] Final `HANDOVER.md`
