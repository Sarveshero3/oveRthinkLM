# What is an RLM (Recursive Language Model)?

## The one-sentence version

An RLM is a wrapper around a regular LLM that gives it a Python REPL and says: "don't read this massive document directly — write code to explore it, and call yourself (or a smaller model) on the pieces you find interesting."

## The full picture

### Step 1: The document becomes a variable

Instead of pasting a 100,000-word document into the prompt, the RLM stores it as a Python variable:

```python
corpus = """[entire 100,000-word document goes here]"""
```

This variable sits inside a running Python session (the REPL). The model never sees the raw text in its prompt.

### Step 2: The model gets metadata, not content

The model's actual prompt looks something like:

```
You have access to a Python REPL with a variable `corpus` containing 
a document of approximately 100,000 words. The document appears to be 
a corporate annual report.

You can write Python code to explore this document. You also have access 
to a function `llm_query(text, question)` that calls an LLM on a piece 
of text.

Question: How many board meetings were held in Q3?

Write code to answer this question.
```

### Step 3: The model writes exploration code

The model generates Python code to investigate:

```python
# First, find relevant sections
sections = corpus.split("QUARTERLY REPORT")
q3_section = sections[3]  # Get Q3

# Search for meeting mentions
import re
meetings = re.findall(r"board meeting.*?held on (\w+ \d+)", q3_section)
print(f"Found {len(meetings)} board meetings in Q3")
print(meetings)
```

### Step 4: The REPL executes the code

The code runs in a sandboxed Python environment. The output gets returned to the model:

```
Found 4 board meetings in Q3
['July 15', 'August 3', 'August 22', 'September 10']
```

### Step 5: The model decides what to do next

After seeing the output, the model can:
- **Answer directly:** "There were 4 board meetings in Q3." (It has enough info.)
- **Explore more:** Write more code to verify or dig deeper.
- **Recurse:** Call `llm_query()` to send a smaller piece of text to another LLM for analysis.

### Step 6 (if recursing): Sub-LLM call

```python
# Ask a sub-model to analyze the Q3 section in detail
result = llm_query(q3_section, "List all board meetings with dates and attendees")
# `result` is now a Python variable, NOT injected into the parent's context
print(result)
```

This is the **recursive** part of RLM. The sub-model gets a smaller, focused piece of text — avoiding the context rot that would hit the parent if it tried to read everything.

## The key design principles

1. **Context as data, not prompt.** The document is a Python variable the model interacts with via code, not raw text crammed into the attention window.

2. **Code as the exploration tool.** The model writes Python to slice, search, count, and extract — it's doing targeted retrieval, not passive reading.

3. **Recursion for depth.** When a section is still too complex, the model delegates to a sub-model. This is what makes it *recursive* — models calling models.

4. **Results as variables.** Sub-call outputs come back as Python variables (`result = llm_query(...)`), not appended to the parent's context. This prevents the parent's context from growing and rotting.

## What an RLM is NOT

- **Not a fine-tuned model.** It's a scaffold around an existing LLM. No training required.
- **Not a coding agent.** The code is specifically for exploring/querying the document, not for building software.
- **Not RAG (Retrieval-Augmented Generation).** RAG retrieves pre-chunked text from a vector database. RLM lets the model decide *how* to chunk and explore, dynamically.
