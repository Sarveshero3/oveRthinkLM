# Machine environment notes — Sarvesh's dev machine

Plain-text record of local machine configuration, kept separate from any single project. Read this first at the start of any new project, any new chat with an LLM or coding agent, or if you're a human picking this machine up cold. Update it whenever another environment-level change gets made — don't let it go stale.

## Hardware

- OS: Windows 11
- GPU: NVIDIA RTX 3050 — limited VRAM. Treat any local model above roughly 2-4B parameters as a real constraint to check, not a formality to skip.
- C: drive: kept intentionally lean, was down to ~55GB free before this cleanup. Default assumption: don't let new tooling install to C: without checking first.
- D: drive: ~499GB free. The default target for anything storage-heavy — container engines, local model weights, build caches.

## Container engine: Podman, not Docker

- Installed via `winget install -e --id RedHat.Podman`
- The Podman machine VM (`podman-machine-default`) has been relocated off C: to `D:\WSL\podman-machine-default`. Any future Podman machine work should assume this location, not the Windows default under `AppData\Local`.
- Docker Desktop's WSL backend (the `docker-desktop` distro) was unregistered to reclaim space. Docker Desktop is not the active container engine on this machine — Podman is. If the Docker Desktop app is ever reopened, expect it to reinitialize its WSL integration from scratch, since its backend was pulled out from under it.
- `podman play kube` — running real Kubernetes-syntax YAML manifests through Podman without a full cluster — is the intended path for anything needing "Kubernetes orchestration" on this machine, since there is no standalone K8s cluster installed.
- Windows build at time of this setup: 10.0.22631.6199.

## Local LLM inference: Ollama

- Model storage relocated off C: via the `OLLAMA_MODELS` environment variable, now pointing at `D:\OllamaModels`. New pulls land there, not the old default `C:\Users\Sarvesh\.ollama\models`.
- Current models: `qwen3:1.7b` (small, GPU-resident on the 3050, the default for lightweight agent/tool-following roles), `nomic-embed-text` (small, embeddings).
- `gemma4:latest` was removed — 9.6GB was too large for this machine's VRAM budget, and it was a superseded generation for this use case anyway (Qwen3 is the current default recommendation as of mid-2026).
- Rule of thumb: don't pull anything above roughly 2-4B parameters on this machine without checking the VRAM fit first. Cloud API is the fallback for anything that actually needs frontier-level reasoning.

## Scope of this file

This file is machine-level only — hardware, storage layout, and locally installed tooling. Project-specific decisions (architecture, requirements, trust mechanisms, whatever a given build actually does) belong in that project's own PRD or kickoff document, not here. Keep this file generic enough to hand to any project or any agent, on day one, before any project-specific context exists.
