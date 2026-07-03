"""Custom state and injected context for the SQL-reflection agent."""

from dataclasses import dataclass

from langchain.agents import AgentState


@dataclass
class DbContext:
    db_path: str


class SqlState(AgentState):
    attempts: int
