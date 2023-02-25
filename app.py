# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.
from dash import Dash, html, dcc, page_container, Input, Output
import pandas as pd
from views.stock import toggle_and_line_chart
from views.header import header

# DEFINE APP
external_stylesheet = 'https://codepen.io/chriddyp/pen/bWLwgP.css'
BS = "https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css"
app = Dash(
    __name__,
    meta_tags=[{"name": "viewport", "content": "width=device-width"}],
    # use_pages=True,
    # external_stylesheets=[external_stylesheet, BS]
)

application = app.server
app.title = f'Stock Data'


app.layout = html.Div(
    [
        header,
        toggle_and_line_chart,
    ]
)

if __name__ == '__main__':
    app.run_server(debug=True)
    # app.run_server(debug=False,dev_tools_ui=False,dev_tools_props_check=False)
