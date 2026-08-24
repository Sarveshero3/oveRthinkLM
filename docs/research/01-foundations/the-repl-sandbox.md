# The REPL Sandbox

## What "REPL" means

REPL stands for **Read-Eval-Print Loop**:

1. **Read** — take in a piece of code
2. **Eval** — execute it
3. **Print** — show the output
4. **Loop** — wait for the next piece of code

If you've ever typed Python into an interactive terminal and seen results immediately, that's a REPL. The RLM engine gives the LLM its own REPL to use.

## What "Sandbox" means

A **sandbox** is an isolated environment where code runs without being able to affect the outside world. Think of it like a playground inside walls — the code can do whatever it wants *inside*, but it can't:

- Read files from your computer
- Access the internet
- Use unlimited memory
- Run forever

## Why isolation matters here

The LLM generates the code that runs in the REPL. We have zero control over what it writes. It might write:

```python
import os; os.system("rm -rf /")  # Delete everything
```

or:

```python
while True: pass  # Infinite loop, freezes the system
```

or:

```python
x = "A" * (10 ** 12)  # Allocate 1 TB of RAM
```

These aren't hypothetical — LLMs produce unexpected code regularly. The sandbox exists to make all of these harmless.

## How sandboxing actually works (our design)

There's a spectrum of isolation, from weakest to strongest:

### ❌ Level 0: Bare `exec()` (NOT acceptable)
```python
exec(model_generated_code)  # Runs in our process, full access to everything
```
This is what we explicitly do NOT do. It's not sandboxing, it's a security hole.

### ❌ Level 1: `exec()` with try/except (NOT acceptable)
```python
try:
    exec(model_generated_code)
except:
    pass
```
Catching errors doesn't prevent the code from deleting files or using all your RAM before the error occurs.

### ✅ Level 2: Subprocess isolation (our minimum)
```python
import subprocess
result = subprocess.run(
    ["python", "-c", model_generated_code],
    timeout=30,           # Kill after 30 seconds
    capture_output=True,  # Capture stdout/stderr
    # + memory limits via OS-level controls
)
```
The code runs in a *separate process*. If it tries to use too much memory, the OS kills it. If it loops forever, the timeout kills it. It can't access our process's variables.

### ✅ Level 3: Container isolation (even better)
Run the code inside a Podman/Docker container with:
- No network access
- Read-only filesystem (except a temp directory)
- CPU and memory limits
- Dropped capabilities (no system calls)

This is what production RLM implementations use (the reference repo `alexzhang13/rlm` supports Docker, Modal, and other sandboxes).

## What the sandbox contains

When the REPL starts for a given query, it has:

| Variable | Contents |
|----------|----------|
| `corpus` (or similar) | The long document being analyzed |
| `llm_query()` function | Callable function to make sub-LLM calls |
| Standard Python builtins | `len()`, `print()`, `re`, `json`, etc. |

And explicitly does NOT have:
- `os`, `sys`, `subprocess` (no system access)
- `requests`, `urllib` (no network)
- `open()` for arbitrary file paths (no filesystem escape)

## The REPL loop in practice

```
┌─────────────────────────────────────────┐
│           RLM Engine                     │
│  (has the model, the prompt, the goal)   │
│                                          │
│  1. Sends generated code to sandbox ──┐  │
│                                       │  │
│  ┌────────────────────────────────────┐│  │
│  │         Sandbox REPL              ││  │
│  │  • corpus = "..."                 ││  │
│  │  • llm_query() available         ││  │
│  │  • Timeout: 30s, Mem: 256MB      ││  │
│  │                                   ││  │
│  │  Executes code, returns output ───┘│  │
│  └────────────────────────────────────┘  │
│                                          │
│  2. Engine reads output                  │
│  3. Decides: answer / explore / recurse  │
│  4. If more code needed, go to step 1    │
└─────────────────────────────────────────┘
```

Each iteration of this loop is one "turn" of the REPL. The full sequence of turns is recorded as the **trajectory**.
