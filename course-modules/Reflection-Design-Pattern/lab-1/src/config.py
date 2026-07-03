"""Configuration for the chart-reflection lab: paths, model, and dataset schema."""

from pathlib import Path

LAB_DIR = Path(__file__).resolve().parent.parent

DATA_DIR = LAB_DIR / "data"
OUTPUT_DIR = LAB_DIR / "outputs"

DATASET_PATH = DATA_DIR / "coffee_sales.csv"
CHART_V1_PATH = OUTPUT_DIR / "chart_v1.png"
CHART_V2_PATH = OUTPUT_DIR / "chart_v2.png"

MODEL_NAME = "gpt-4.1-mini"
TEMPERATURE = 0

INSTRUCTION = "Create a plot comparing Q1 coffee sales in 2024 and 2025."

SCHEMA = """
coffee_sales.csv columns:
- date: sale date
- time: sale time
- cash_type: cash or card
- card: anonymized card id
- price: sale amount / revenue
- coffee_name: coffee product name
- quarter: quarter number
- month: month number
- year: year
"""
