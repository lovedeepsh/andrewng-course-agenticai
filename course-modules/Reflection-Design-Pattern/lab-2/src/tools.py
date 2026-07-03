"""Tools for the SQL-reflection agent."""

from langchain.messages import ToolMessage
from langchain.tools import ToolRuntime, tool
from langgraph.types import Command

from .db import execute_sql
from .state import DbContext, SqlState


@tool
def run_sql(query: str, runtime: ToolRuntime[DbContext, SqlState]) -> Command:
    """Run a read-only SQLite SELECT and return the resulting rows (or the error).

    Args:
        query: A single SQLite SELECT statement.
    """
    db_path = runtime.context.db_path
    df = execute_sql(query, db_path)
    attempts = runtime.state.get("attempts", 0) + 1
    return Command(
        update={
            "attempts": attempts,
            "messages": [
                ToolMessage(content=df.to_string(index=False), tool_call_id=runtime.tool_call_id)
            ],
        }
    )

