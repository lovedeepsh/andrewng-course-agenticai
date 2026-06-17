from IPython.display import display, HTML
import pandas as pd

def print_html(df, title=None, border=0, max_rows=None, index=False):
    html_table = df.to_html(
    border=border,
    max_rows=max_rows,
    index=index
    )

    html_table = html_table.replace(
        '<table border="1" class="dataframe">',
        '<table border="1" class="dataframe" style="border-collapse: collapse;">'
    ).replace(
        '<th>',
        '<th style="border: 1px solid black; padding: 6px;">'
    ).replace(
        '<td>',
        '<td style="border: 1px solid black; padding: 6px;">'
    )
    heading = HTML(f"<h3>{title}</h3>")
    if title is not None:
        display(heading)
    #return display(HTML(html_table))
    display(HTML(html_table))

def load_and_prepare_data(file_path: str):
    df = pd.read_csv(file_path)
    df["date"] = pd.to_datetime(df["date"])
    df["price"] = pd.to_numeric(df["price"])
    df = df.assign(quarter=df["date"].dt.quarter)
    df = df.assign(month=df["date"].dt.month)
    df = df.assign(year=df["date"].dt.year)
    #pd.DataFrame
    return df