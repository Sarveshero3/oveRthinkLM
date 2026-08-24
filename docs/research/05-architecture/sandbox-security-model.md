# Sandbox Security Model

## Threat Model
The RLM engine asks LLMs to write arbitrary Python code. If untrusted inputs or prompt injections occur, the LLM might emit malicious system calls (`os.remove`, network sockets, CPU starvation, memory leaks).

## Defense in Depth
1. **Subprocess Boundary**: Code runs in an isolated child process spawned with dedicated pipes (`stdin`, `stdout`, `stderr`), not inside the host engine process.
2. **Resource Hardening**:
   - `timeout=30s`: Hard kill on infinite loops.
   - Memory limits: OS-enforced virtual memory ceilings.
3. **Module Whitelisting**: Standard libraries for string processing (`re`, `json`, `math`, `collections`) are permitted; dangerous modules (`os`, `sys`, `subprocess`, `socket`) are blocked from import.
4. **Variable Scoping**: `corpus` is injected in the isolated execution namespace. Sub-call outputs are bound to specific local variables.
