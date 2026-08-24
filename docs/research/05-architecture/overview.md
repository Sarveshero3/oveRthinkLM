# Architecture Overview

```
                        +-----------------------------------------+
                        ¦              Client / CLI               ¦
                        +-----------------------------------------+
                                             ¦ HTTP
                                             ?
                        +-----------------------------------------+
                        ¦               RLM Engine                ¦
                        ¦      (FastAPI Orchestration Core)       ¦
                        ¦                                         ¦
                        ¦  • Decides explore / recurse / answer   ¦
                        ¦  • Handles 6 configuration execution    ¦
                        ¦  • Trajectory recorder & span tracker   ¦
                        +-----------------------------------------+
                                ¦                         ¦
                   Executes Code¦             Sub-LLM Call¦
                                ?                         ?
               +-------------------------+   +-------------------------+
               ¦    Isolated Sandbox     ¦   ¦      Sub-LLM Caller     ¦
               ¦   (Subprocess / REPL)   ¦   ¦  (3-Tier LLM Gateway)   ¦
               ¦                         ¦   ¦                         ¦
               ¦ • Memory limit: 256MB   ¦   ¦ • Tier 1: Local Ollama  ¦
               ¦ • CPU timeout: 30s      ¦   ¦ • Tier 2: Groq LPU API  ¦
               ¦ • Context variable store¦   ¦ • Tier 3: Together.ai   ¦
               +-------------------------+   +-------------------------+
                                ¦                         ¦
                                +-------------------------+
                                             ¦ Logs Trajectories
                                             ?
                        +-----------------------------------------+
                        ¦          Trajectory Dashboard           ¦
                        ¦     (Recursive Call Tree Visualizer)    ¦
                        +-----------------------------------------+
```
