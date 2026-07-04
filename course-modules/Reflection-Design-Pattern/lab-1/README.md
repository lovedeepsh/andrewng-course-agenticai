# Reflection Design Pattern — Lab 1: Chart Reflection

An agent that generates a chart, looks at its own output, critiques it, and
regenerates an improved version. Based on the Reflection design pattern from
Andrew Ng's *Agentic AI* course (DeepLearning.AI), rewritten as a clean,
importable Python project.

## Structure

```
chart_reflection (this lab)
  notebook.ipynb     # narrative + demo; imports from src
  src/
    config.py        # settings the agent must NOT decide (model, paths, schema)
    rendering.py     # display helpers (print_html, encode_image_b64)
    tools.py         # @tool factories (config captured via closures)
    schemas.py       # Pydantic models for structured output
    agent.py         # build_agent(): model + tools + system prompt
  data/              # input csv
  outputs/           # generated charts (gitignored)
```

## Design decisions (what I changed and why)

- A tool's parameters are **decisions the LLM must make**, so the parameters
  should only ever be things the agent genuinely chooses.
- I do **not** let the LLM decide things that are already fixed and known —
  which model to use, the dataset schema, the output filename. Those are
  config, captured by a closure, not tool arguments.
- The `@tool` docstring is the **only** thing the LLM sees to decide whether
  and when to call a tool. In a normal function a docstring is for humans; in
  a tool it is part of the prompt, so it matters more.
- The LLM never touches the dataframe (`df`); it is captured from the outer
  factory function via a closure. The decision is removed from the model.
- Curly braces around a variable (`{model}`) create a **set**, not the value.
  The correct call is `model=model`. (This was a real bug in my first version.)
- Typed/structured output (Pydantic + `with_structured_output`) is a cleaner
  way to get data back than scraping `<execute_python>` tags with regex.
- Return-type annotations must match what the function actually returns:
  a function returning a string is `-> str`; one returning a dict is `-> dict`.

## References (what I read)

- LangChain — Tools: https://docs.langchain.com/oss/python/langchain/tools
- LangChain — Structured output: https://docs.langchain.com/oss/python/langchain/structured-output
- LangChain — Agents (`create_agent`): https://docs.langchain.com/oss/python/langchain/agents
