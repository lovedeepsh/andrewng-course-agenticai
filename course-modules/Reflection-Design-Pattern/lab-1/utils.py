from IPython.display import display, HTML
import html
import pandas as pd
import base64
from typing import Any

# def print_html(df, title=None, border=0, max_rows=None, index=False):
#     html_table = df.to_html(
#     border=border,
#     max_rows=max_rows,
#     index=index
#     )

#     html_table = html_table.replace(
#         '<table border="1" class="dataframe">',
#         '<table border="1" class="dataframe" style="border-collapse: collapse;">'
#     ).replace(
#         '<th>',
#         '<th style="border: 1px solid black; padding: 6px;">'
#     ).replace(
#         '<td>',
#         '<td style="border: 1px solid black; padding: 6px;">'
#     )
#     heading = HTML(f"<h3>{title}</h3>")
#     if title is not None:
#         display(heading)
#     #return display(HTML(html_table))
#     display(HTML(html_table))

## My code is too basic, using course utils.py code
def print_html(content: Any, title: str | None = None, is_image: bool = False):
    """
    Pretty-print inside a styled card.
    - If is_image=True and content is a string: treat as image path/URL and render <img>.
    - If content is a pandas DataFrame/Series: render as an HTML table.
    - Otherwise (strings/others): show as code/text in <pre><code>.
    """
    try:
        from html import escape as _escape
    except ImportError:
        _escape = lambda x: x

    def image_to_base64(image_path: str) -> str:
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode("utf-8")

    # Render content
    if is_image and isinstance(content, str):
        b64 = image_to_base64(content)
        rendered = f'<img src="data:image/png;base64,{b64}" alt="Image" style="max-width:100%; height:auto; border-radius:8px;">'
    elif isinstance(content, pd.DataFrame):
        rendered = content.to_html(classes="pretty-table", index=False, border=0, escape=False)
    elif isinstance(content, pd.Series):
        rendered = content.to_frame().to_html(classes="pretty-table", border=0, escape=False)
    elif isinstance(content, str):
        rendered = f"<pre><code>{_escape(content)}</code></pre>"
    else:
        rendered = f"<pre><code>{_escape(str(content))}</code></pre>"

    css = """
    <style>
    .pretty-card{
      font-family: ui-sans-serif, system-ui;
      border: 2px solid transparent;
      border-radius: 14px;
      padding: 14px 16px;
      margin: 10px 0;
      background: linear-gradient(#fff, #fff) padding-box,
                  linear-gradient(135deg, #3b82f6, #9333ea) border-box;
      color: #111;
      box-shadow: 0 4px 12px rgba(0,0,0,.08);
    }
    .pretty-title{
      font-weight:700;
      margin-bottom:8px;
      font-size:14px;
      color:#111;
    }
    /* 🔒 Only affects INSIDE the card */
    .pretty-card pre, 
    .pretty-card code {
      background: #f3f4f6;
      color: #111;
      padding: 8px;
      border-radius: 8px;
      display: block;
      overflow-x: auto;
      font-size: 13px;
      white-space: pre-wrap;
    }
    .pretty-card img { max-width: 100%; height: auto; border-radius: 8px; }
    .pretty-card table.pretty-table {
      border-collapse: collapse;
      width: 100%;
      font-size: 13px;
      color: #111;
    }
    .pretty-card table.pretty-table th, 
    .pretty-card table.pretty-table td {
      border: 1px solid #e5e7eb;
      padding: 6px 8px;
      text-align: left;
    }
    .pretty-card table.pretty-table th { background: #f9fafb; font-weight: 600; }
    </style>
    """

    title_html = f'<div class="pretty-title">{title}</div>' if title else ""
    card = f'<div class="pretty-card">{title_html}{rendered}</div>'
    display(HTML(css + card))

def print_code_html(code: str, title=None):
    if title is not None:
        display(HTML(f"<h3>{html.escape(title)}</h3>"))

    escaped_code = html.escape(code)

    display(HTML(f"""
    <pre style="
        border: 1px solid black;
        padding: 12px;
        border-radius: 6px;
        background-color: #f7f7f7;
        white-space: pre-wrap;
        font-family: monospace;
    ">{escaped_code}</pre>
    """))

def load_and_prepare_data(file_path: str):
    df = pd.read_csv(file_path)
    df["date"] = pd.to_datetime(df["date"])
    df["price"] = pd.to_numeric(df["price"])
    df = df.assign(quarter=df["date"].dt.quarter)
    df = df.assign(month=df["date"].dt.month)
    df = df.assign(year=df["date"].dt.year)
    #pd.DataFrame
    return df
import mimetypes
def encode_image_b64(path: str) -> tuple[str, str]:
    """Return (media_type, base64_str) for an image file path."""
    mime, _ = mimetypes.guess_type(path)
    media_type = mime or "image/png"
    with open(path, "rb") as f:
        b64 = base64.b64encode(f.read()).decode("utf-8")
    return media_type, b64