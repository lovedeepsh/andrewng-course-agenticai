"""Custom state and injected context for the chart-reflection agent."""

from dataclasses import dataclass

import pandas as pd
from langchain.agents import AgentState


@dataclass
class ChartContext:
    df: pd.DataFrame


class ChartState(AgentState):
    attempts: int
