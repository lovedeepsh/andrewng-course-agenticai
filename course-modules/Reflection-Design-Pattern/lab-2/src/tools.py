"""Tools for the SQL-reflection agent."""

from langchain_core.tools import tool
from langchain_openai import ChatOpenAI

from . import config
from .db import execute_sql
from .schemas import SqlQuery, SqlReflection


def make_sql_tools(
    schema: str,
    instruction: str,
    model_name: str,
    db_path: str,
):
    """Create the SQL-generation and SQL-reflection tools.

    Config (schema, question, model, db path) is captured in the closure so the
    tools take no arguments. The shared ``ctx`` dict passes the first query and
    its result from the generation step to the reflection step.

    Returns:
        A ``(generate_sql_v1, reflect_and_regenerate_sql)`` tuple.
    """
    ctx: dict = {}

    @tool
    def generate_sql_v1() -> str:
        """Write the first SQL query for the question and run it."""
        prompt = f"""
        You are a senior data analyst. 
        Your task: I will share you a question and dataset schema.
        Based on the question and dataset schema, write a SQLite SELECT query to answer the question.
        Do not explain anything.

        Dataset schema:
        {schema}

        User instructions:
        {instruction}
        """
        llm = ChatOpenAI(model=model_name, temperature=config.TEMPERATURE)
        result = llm.with_structured_output(SqlQuery).invoke(prompt)
        df = execute_sql(result.sql, db_path)
        ctx["sql_v1"] = result.sql
        ctx["result_v1"] = df
        return result.sql

    @tool
    def reflect_and_regenerate_sql() -> str:
        """Critique the first query and its result, then produce an improved query."""
        sql_v1 = ctx.get("sql_v1", "")
        result_v1 = ctx.get("result_v1")
        result_preview = result_v1.to_string() if result_v1 is not None else "(no result available)"
        prompt = f"""
        You are a senior data analyst.
        Your task: I will share you a question, dataset schema, SQLite SELECT query and its result.
        Analyze the query and its result from correctness, efficiency and readability perspective.
        Then gather your feedback and re-create a new query for me.
        Do not explain anything.
        
        Dataset schema:
        {schema}

        Question to answer:
        {instruction}

        SQLite SELECT query:
        {sql_v1}

        Result preview:
        {result_preview}
        """
        llm = ChatOpenAI(model=model_name, temperature=config.TEMPERATURE)
        result = llm.with_structured_output(SqlReflection).invoke(prompt)
        df = execute_sql(result.sql, db_path)
        return f"Feedback:\n{result.feedback}\n\nImproved SQL:\n{result.sql}"

    return generate_sql_v1, reflect_and_regenerate_sql
