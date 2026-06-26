"""Builds the chart-reflection agent: model, tools, and system prompt."""

import pandas as pd
from langchain.agents import create_agent
from langchain.chat_models import init_chat_model
from langgraph.checkpoint.memory import InMemorySaver

from . import config
from .tools import make_reflection_tools

SYSTEM_PROMPT = """\
You are a data-visualization expert. You improve charts in two steps: first
generate a chart, then reflect on it and produce a better one. Call your tools
in order. Do not ask the user questions.
"""


def build_agent(df: pd.DataFrame):
    """Assemble and return the chart-reflection agent."""
    generate_chart, reflect_and_regenerate = make_reflection_tools(
        df=df, schema=config.SCHEMA, instruction=config.INSTRUCTION,
        model_name=config.MODEL_NAME,
        v1_path=str(config.CHART_V1_PATH), v2_path=str(config.CHART_V2_PATH),
    )
    model = init_chat_model(f"openai:{config.MODEL_NAME}", temperature=config.TEMPERATURE)
    return create_agent(
        model=model, tools=[generate_chart, reflect_and_regenerate],
        system_prompt=SYSTEM_PROMPT, checkpointer=InMemorySaver(),
    )
