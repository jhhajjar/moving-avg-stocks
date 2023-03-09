# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.
from views.header import header
from views.stock import toggle_and_line_chart
from dash import Dash, html

# DEFINE APP
app = Dash(
    __name__,
    meta_tags=[{"name": "viewport", "content": "width=device-width"}]
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
