"""Pydantic schemas for structured model output."""

from pydantic import BaseModel, Field


class SqlQuery(BaseModel):
    """A single SQL query."""

    sql: str = Field(description="One runnable SQLite SELECT query. No prose, no markdown fences.")


class SqlReflection(BaseModel):
    """A critique of a query and its result, plus an improved query."""

    feedback: str = Field(description="Concise critique of the previous query and its result.")
    sql: str = Field(description="Improved runnable SQLite SELECT query. No prose, no markdown fences.")
