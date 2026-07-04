"""Configuration for the Tool-Use lab: model and paths."""

from pathlib import Path

LAB_DIR = Path(__file__).resolve().parent.parent

OUTPUT_DIR = LAB_DIR / "outputs"
ASSETS_DIR = LAB_DIR / "assets"

MODEL = "openai:gpt-4o"
