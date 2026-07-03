"""Tools for the chart-reflection agent."""

from langchain.messages import ToolMessage
from langchain.tools import ToolRuntime, tool
from langgraph.types import Command

from .state import ChartContext, ChartState


@tool
def run_python(code: str, runtime: ToolRuntime[ChartContext, ChartState]) -> Command:
    """Execute pandas + matplotlib code. A DataFrame named `df` is already available.

    Args:
        code: Runnable Python that builds a chart and calls plt.savefig(...).
    """
    df = runtime.context.df
    try:
        exec(code, {"df": df})
        message = "Code ran successfully; chart saved."
    except Exception as e:
        message = f"Error running code: {e}"
    attempts = runtime.state.get("attempts", 0) + 1
    return Command(
        update={
            "attempts": attempts,
            "messages": [ToolMessage(content=message, tool_call_id=runtime.tool_call_id)],
        }
    )
