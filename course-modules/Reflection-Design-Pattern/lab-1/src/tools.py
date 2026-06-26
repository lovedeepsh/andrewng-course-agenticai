"""Tools for the chart-reflection agent."""

import pandas as pd
from langchain_core.messages import HumanMessage
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI

from . import config
from .rendering import encode_image_b64
from .schemas import ChartCode, ChartReflection


def make_reflection_tools(
    df: pd.DataFrame,
    schema: str,
    instruction: str,
    model_name: str,
    v1_path: str,
    v2_path: str,
):
    """Create the chart-generation and reflection tools.

    Configuration (dataframe, schema, model, output paths) is captured here so
    the tools take no arguments. The shared ``ctx`` dict passes the first
    chart's code from the generation step to the reflection step.

    Returns:
        A ``(generate_chart_v1, reflect_and_regenerate)`` tuple.
    """
    ctx: dict = {}

    @tool
    def generate_chart_v1() -> str:
        """Generate and run code for the first version of the requested chart."""
        prompt = f"""You are a Python data analyst.
        A pandas DataFrame named `df` is already loaded in scope. Do not read any CSV
        and do not recreate the dataframe. We already have that ready as df.

        Dataset schema:
        {schema}

        Task:
        {instruction}
        Do not explain anything and do not create the dataframe again.
        We already have that ready as df.

        Rules:
        - Use pandas and matplotlib only.
        - Save the chart to '{v1_path}'.
        - Return runnable Python code only. No prose, no markdown fences.
        """
        llm = ChatOpenAI(model=model_name, temperature=config.TEMPERATURE)
        result = llm.with_structured_output(ChartCode).invoke(prompt)
        ctx["code_v1"] = result.code
        exec(result.code, {"df": df})
        return result.code

    @tool
    def reflect_and_regenerate() -> str:
        """Critique the first chart and produce an improved second version."""
        code_v1 = ctx.get("code_v1", "")
        media_type, b64 = encode_image_b64(v1_path)
        prompt = f"""
        You are a Python data analyst.
        Your task: I will share you a chart png file and python code which generated that chart.
        Visualize the chart & code, further analyze it from clarity, labeling, accuracy and overall readability perspective.
        Then gather your feedback and re-create a new code python code for me in structured format.

        Dataset schema:
        {schema}

        User instructions:
        {instruction}

        code:
        {code_v1}

        Rules:
        - Use pandas and matplotlib only.
        - Return Python code in structured format.
        - Save the output chart as '{v2_path}'.
        - Do not create the dataframe again, we already have that ready as df
        - datetime is already datetime object
        - Do not explain anything and I expect 2 things from you and nothing i.e. feedback and python code
        """
        llm = ChatOpenAI(model=model_name, temperature=config.TEMPERATURE)
        message = HumanMessage(content=[
            {"type": "text", "text": prompt},
            {"type": "image_url", "image_url": {"url": f"data:{media_type};base64,{b64}"}},
        ])
        result = llm.with_structured_output(ChartReflection).invoke([message])
        exec(result.code, {"df": df})
        return f"Feedback:\n{result.feedback}\n\nImproved code:\n{result.code}"

    return generate_chart_v1, reflect_and_regenerate
