"""Builds the SQL-reflection agent."""

from langchain.agents import create_agent
from langchain.chat_models import init_chat_model
from langgraph.checkpoint.memory import InMemorySaver

from . import config
from .db import get_schema
from .state import DbContext, SqlState
from .tools import run_sql

SYSTEM_PROMPT = """\
You are a senior data analyst. Answer the question by writing a SQLite SELECT
query and calling run_sql to execute it.

Work in two steps:
1. Write a first query and run it with run_sql.
2. Look at the rows it returned. If the result is wrong, empty, or could be more
   correct or clearer, refine the query and run it again.

Table schema:
{schema}

When you are satisfied, reply with the final SQL and a one-line summary of the
result. Do not ask the user questions.
"""


def build_agent():
    schema = get_schema(str(config.DB_PATH))
    model = init_chat_model(f"openai:{config.MODEL_NAME}", temperature=config.TEMPERATURE)
    return create_agent(
        model=model,
        tools=[run_sql],
        system_prompt=SYSTEM_PROMPT.format(schema=schema),
        state_schema=SqlState,
        context_schema=DbContext,
        checkpointer=InMemorySaver(),
    )

