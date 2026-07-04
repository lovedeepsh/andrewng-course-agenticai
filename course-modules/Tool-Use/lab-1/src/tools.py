"""Tools the LLM can call.

Each function's docstring IS the description LangChain hands to the LLM, and the
parameters become the tool's input schema. So docstrings and type hints are not
decoration here — they are how the model decides when and how to call a tool.
The ``@tool`` decorator turns each plain function into a LangChain tool.
"""

from datetime import datetime

import qrcode
import requests
from langchain_core.tools import tool
from qrcode.image.styledpil import StyledPilImage

from . import config

@tool
def get_current_time() -> str:
    """Returns the current time as a string."""

    return datetime.now().strftime("%H:%M:%S")

@tool
def write_txt_file(file_path: str, content: str) -> str:
    """Write a string into a .txt file (overwrites if it exists).

    Args:
        file_path: Destination path for the file.
        content: Text to write into the file.

    Returns:
        The path to the written file.
    """

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)
    return file_path

@tool
def get_weather_from_ip() -> str:
    """Gets the current, high, and low temperature (Fahrenheit) for the user's location."""
    lat, lon = requests.get("https://ipinfo.io/json").json()["loc"].split(",")
    params = {
        "latitude": lat,
        "longitude": lon,
        "current": "temperature_2m",
        "daily": "temperature_2m_max,temperature_2m_min",
        "temperature_unit": "fahrenheit",
        "timezone": "auto",
    }
    data = requests.get("https://api.open-meteo.com/v1/forecast", params=params).json()
    return (
        f"Current: {data['current']['temperature_2m']}°F, "
        f"High: {data['daily']['temperature_2m_max'][0]}°F, "
        f"Low: {data['daily']['temperature_2m_min'][0]}°F"
    )

@tool
def generate_qr_code(data: str, filename: str, image_path: str | None = None) -> str:
    """Generate a QR code PNG from data, optionally embedding a center image.

    Args:
        data: Text or URL to encode.
        filename: Output file name without extension (saved under outputs/).
        image_path: Optional path to a logo to embed in the QR code.
    """
    qr = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_H)
    qr.add_data(data)
    if image_path:
        img = qr.make_image(image_factory=StyledPilImage, embedded_image_path=image_path)
    else:
        img = qr.make_image()
    output_file = str(config.OUTPUT_DIR / f"{filename}.png")
    img.save(output_file)
    return f"QR code saved as {output_file} containing: {data[:50]}..."
