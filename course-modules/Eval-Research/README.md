# Eval & Research — Component-level evaluation

Evaluate one component of a research agent — the web-search/research step — with an
objective, per-example check: do the returned sources come from preferred domains?

## Structure

```
Eval-Research/
  notebook.ipynb        # the demo (thin)
  src/
    config.py           # model, task, TOP_DOMAINS, MIN_RATIO
    research.py         # find_references() — runs the arxiv/tavily/wikipedia tools
    research_tools.py   # the tool definitions (provided)
    evaluation.py       # evaluate_tavily_results()  <- you write this
    rendering.py        # print_html display helper
```

## Setup

1. Install dependencies into the repo venv:

   ```bash
   # langchain/langchain-openai/langgraph are already installed from the reflection labs;
   # these are the extras this lab's tools need:
   uv add tavily-python wikipedia requests
   ```

2. Add a Tavily key to the repo-root `.env` (Tavily powers the web search):

   ```
   TAVILY_API_KEY=tvly-...
   ```

   (Outside the DeepLearning.AI platform, leave `DLAI_TAVILY_BASE_URL` unset so the
   Tavily client uses its default endpoint.)

3. Open `notebook.ipynb`, select the **andrewng-course** kernel, and Run All.

## Note

The old top-level `utils.py` is now dead (its `print_html` moved to
`src/rendering.py`, and the eval lives in `src/evaluation.py`). You can delete it,
along with the top-level `research_tools.py` (now in `src/`).
