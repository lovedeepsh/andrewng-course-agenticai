"""Display helper for rendering text/JSON inside a styled card."""

from typing import Any

from IPython.display import HTML, display

def print_html(content: Any, title: str | None = None):
    """Pretty-print a string (e.g. JSON) inside a styled card."""
    try:
        from html import escape as _escape
    except ImportError:
        _escape = lambda x: x

    rendered = f"<pre><code>{_escape(str(content))}</code></pre>"
    css = """
    <style>
    .pretty-card{font-family: ui-sans-serif, system-ui; border: 2px solid transparent;
      border-radius: 14px; padding: 14px 16px; margin: 10px 0;
      background: linear-gradient(#fff, #fff) padding-box,
                  linear-gradient(135deg, #3b82f6, #9333ea) border-box;
      color: #111; box-shadow: 0 4px 12px rgba(0,0,0,.08);}
    .pretty-title{font-weight:700; margin-bottom:8px; font-size:14px; color:#111;}
    .pretty-card pre, .pretty-card code{background:#f3f4f6; color:#111; padding:8px;
      border-radius:8px; display:block; overflow-x:auto; font-size:13px; white-space:pre-wrap;}
    </style>
    """
    title_html = f'<div class="pretty-title">{title}</div>' if title else ""
    display(HTML(css + f'<div class="pretty-card">{title_html}{rendered}</div>'))
