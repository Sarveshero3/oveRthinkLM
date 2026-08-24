# Research Documentation — oveRthinkLM

This folder is a structured knowledge base organized as a folder-based mindmap. Read in order of the numbered folders to build understanding from the ground up.

## Structure

```
docs/research/
+-- 01-foundations/          ? What the core concepts are
¦   +-- context-rot.md
¦   +-- what-is-an-rlm.md
¦   +-- the-repl-sandbox.md
¦   +-- sub-llm-calls.md
¦   +-- recursion-depth.md
+-- 02-the-three-papers/     ? The research debate this project investigates
¦   +-- original-rlm-zhang-2025.md
¦   +-- think-but-dont-overthink-wang-2026.md
¦   +-- srlm-uncertainty-apple-2026.md
+-- 03-uncertainty-signals/  ? How SRLM's mechanism works (no public code exists)
¦   +-- self-consistency.md
¦   +-- verbalized-confidence.md
¦   +-- reasoning-length.md
¦   +-- how-they-combine.md
+-- 04-six-configurations/   ? Deep dive into the 6 configurations compared
¦   +-- 01-depth-0-baseline.md
¦   +-- 02-depth-1-rlm.md
¦   +-- 03-depth-2-rlm.md
¦   +-- 04-srlm-self-reflection.md
¦   +-- 05-hybrid-1.md
¦   +-- 06-hybrid-2.md
+-- 05-architecture/         ? How the system components fit together
¦   +-- overview.md
¦   +-- sandbox-security-model.md
¦   +-- three-tier-llm-routing.md
+-- 06-design-decisions/     ? Architectural decisions during grill-with-docs
¦   +-- hybrid-uncertainty-integration.md
+-- 07-devops-pipeline/      ? Containers, CI/CD, monitoring
    +-- (populated during later phases)
```

Each document is self-contained. Read `01-foundations/` first if you're new to RLMs.
