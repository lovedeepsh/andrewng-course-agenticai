"""Configuration for the SQL-reflection lab: paths, model, and the question."""

from pathlib import Path

LAB_DIR = Path(__file__).resolve().parent.parent

DB_PATH = LAB_DIR / "products.db"

MODEL_NAME = "gpt-4.1-mini"
TEMPERATURE = 0

# The analytics question (fixed for this lab). The schema is read from the DB
# at build time, so it is not stored here.
INSTRUCTION = (
    "Find the top 5 products by total units sold. "
    "Units sold = the absolute number of units from 'sale' events. "
    "Return product_name and total_units_sold, ordered by total_units_sold descending."
)
