# Tool Use — Lab 2: Email Assistant Agent

An aisuite tool-calling agent over a simulated FastAPI email backend. The agent
takes natural-language requests and chains email tools (search, mark read, send,
delete) to fulfil them.

## Structure

```
lab-2/
  notebook.ipynb        # the demos (thin)
  src/
    config.py           # models, MAX_TURNS, USER_EMAIL
    email_tools.py       # HTTP client tools that call the email server
    prompts.py          # build_prompt() system preamble
    rendering.py        # print_html display helper
    display_functions.py # pretty_print_chat_completion (tool-call trace)
  email_server/         # the FastAPI backend (run it; do not edit)
```

## Setup

1. Install dependencies into the repo venv:

   ```bash
   # langchain/langchain-openai/langgraph are already installed from the reflection labs;
   # these are the extras this lab's server needs:
   uv add fastapi "uvicorn[standard]" sqlalchemy jinja2 requests
   ```

2. Point the tools at the server — add to the repo-root `.env`:

   ```
   M3_EMAIL_SERVER_API_URL=http://127.0.0.1:8000
   ```

3. Start the email server in a separate terminal, from this lab folder, and
   leave it running:

   ```bash
   cd course-modules/Tool-Use/lab-2
   uv run uvicorn email_server.email_service:app --port 8000
   ```

   The tools in `src/email_tools.py` call this server over HTTP. Check it's up:
   `http://127.0.0.1:8000/health` should return `{"status": "ok"}`.

4. Open `notebook.ipynb`, select the **andrewng-course** kernel, and Run All.
   Re-run `email_tools.reset_database()` any time to restore the test inbox.
