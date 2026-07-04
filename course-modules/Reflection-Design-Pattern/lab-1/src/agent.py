"""Builds the chart-reflection agent."""

from langchain.agents import create_agent
from langchain.chat_models import init_chat_model
from langgraph.checkpoint.memory import InMemorySaver

from . import config
from .state import ChartContext, ChartState
from .tools import run_python

SYSTEM_PROMPT = """\
You are a data-visualization expert. Answer the task by writing pandas +
matplotlib code and calling run_python to execute it. A pandas DataFrame named
`df` is already loaded (schema below). Do not read any CSV.

Work in two steps:
1. Write code that builds the chart and saves it to '{v1_path}', then run it.
2. Review your own code for correctness and clarity (correct filtering, the right
   comparison, a title, axis labels, a legend, a sensible chart type). Write
   improved code that saves to '{v2_path}' and run it. If run_python reports an
   error, fix it and run again.

Dataset schema:
{schema}

Task:
{instruction}

Do not ask the user questions.
"""


def build_agent():
    model = init_chat_model(f"openai:{config.MODEL_NAME}", temperature=config.TEMPERATURE)
    prompt = SYSTEM_PROMPT.format(
        v1_path=str(config.CHART_V1_PATH),
        v2_path=str(config.CHART_V2_PATH),
        schema=config.SCHEMA,
        instruction=config.INSTRUCTION,
    )
    return create_agent(
        model=model,
        tools=[run_python],
        system_prompt=prompt,
        state_schema=ChartState,
        context_schema=ChartContext,
        checkpointer=InMemorySaver(),
    )

