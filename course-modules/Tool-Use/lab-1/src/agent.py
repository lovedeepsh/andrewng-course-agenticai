"""Builds the tool-use agent: model, tools, and system prompt."""

from langchain.agents import create_agent
from langchain.chat_models import init_chat_model
from langgraph.checkpoint.memory import InMemorySaver

from . import config

SYSTEM_PROMPT = """\
You are a helpful assistant that uses the tools available to answer the user's
request. Do not ask the user questions.
"""

def build_agent(tools):
    """Assemble and return the tool-use agent."""

    model = init_chat_model(config.MODEL)
    return create_agent(model=model, tools=tools, system_prompt=SYSTEM_PROMPT, checkpointer=InMemorySaver())
