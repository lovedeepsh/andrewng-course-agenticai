"""Builds the email-assistant agent: model, tools, and system prompt."""

from langchain.agents import create_agent
from langchain.chat_models import init_chat_model
from langgraph.checkpoint.memory import InMemorySaver

from . import config

SYSTEM_PROMPT = f"""\
- You are an AI assistant specialized in managing emails.
- You can perform actions such as listing, searching, filtering, and manipulating emails.
- Use the provided tools to interact with the email system.
- Never ask the user for confirmation before performing an action.
- If needed, my email address is "{config.USER_EMAIL}" so you can use it to send emails or perform actions related to my account.
"""

def build_agent(tools):
    """Assemble and return the email-assistant agent.

    Args:
        tools: The list of ``@tool`` objects (StructuredTools) the agent may
            call. The set of tools you pass in defines what the agent can do.

    Returns:
        A compiled LangChain agent.
    """

    model = init_chat_model(config.MODEL)
    return create_agent(model=model, tools=tools, system_prompt=SYSTEM_PROMPT, checkpointer=InMemorySaver())
