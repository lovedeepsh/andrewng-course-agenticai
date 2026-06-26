"""Pydantic schemas for structured model output."""

from pydantic import BaseModel, Field


class ChartCode(BaseModel):
    """Runnable code for a chart."""

    code: str = Field(description="Runnable pandas+matplotlib code. No prose, no markdown fences.")


class ChartReflection(BaseModel):
    """A critique of a chart and improved code for the next version."""

    feedback: str = Field(description="Concise critique of the chart.")
    code: str = Field(description="Improved runnable pandas+matplotlib code. No prose, no markdown fences.")
