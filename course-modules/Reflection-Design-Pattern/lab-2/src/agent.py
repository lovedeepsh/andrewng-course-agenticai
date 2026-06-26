"""Builds the SQL-reflection agent: model, tools, and system prompt."""

from langchain.agents import create_agent
from langchain.chat_models import init_chat_model
from langgraph.checkpoint.memory import InMemorySaver

from . import config
from .db import get_schema
from .tools import make_sql_tools

SYSTEM_PROMPT = """\
You are a senior data analyst. You answer questions in two steps: first write a
SQL query, then reflect on the query and its result and produce a better one.
Call your tools in order. Do not ask the user questions.
"""


def build_agent():
    """Assemble and return the SQL-reflection agent.

    Note: no ``df`` argument here (unlike lab-1) — this lab reads from the DB,
    and the schema is fetched from the DB at build time.
    """
    schema = get_schema(str(config.DB_PATH))
    v1_tool, v2_tool = make_sql_tools(
        schema=schema, instruction=config.INSTRUCTION,
        model_name=config.MODEL_NAME, db_path=str(config.DB_PATH),
    )
    model = init_chat_model(f"openai:{config.MODEL_NAME}", temperature=config.TEMPERATURE)
    return create_agent(
        model=model, tools=[v1_tool, v2_tool],
        system_prompt=SYSTEM_PROMPT, checkpointer=InMemorySaver(),
    )
