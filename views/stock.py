import numpy as np
from dash.exceptions import PreventUpdate
from datetime import date, datetime
from utils import get_data, multi_line_plot, find_intersections, add_avgs, calc_percents, get_margins, melt_intersections
from dash import Input, Output, callback, dcc, html, dash_table

toggle_and_line_chart = html.Div(
    [
        html.Div(
            [
                dcc.Store(id="dataframe"),
                dcc.Store(id="company_name"),
                html.Div(
                    [
                        html.P("Choose TICKER:", className="control_label"),
                        dcc.Dropdown(
                            id="ticker-dropdown",
                            value="TSLA",
                            options=["TSLA", "MSFT", "VTI", "FL"],
                            multi=False,
                            className="dcc_control dropdown_black",
                            style={"color": "black"},
                        ),
                        html.Div(
                            [
                                html.Div([
                                    html.P("Start Date:"),
                                    dcc.DatePickerSingle(
                                        id='start-date',
                                        min_date_allowed=date(1995, 1, 1),
                                        max_date_allowed=datetime.now().date(),
                                        date=date(2020, 1, 1),
                                    ),
                                ],
                                    style={"float": "left"}
                                ),
                                html.Div([
                                    html.P("End Date:"),
                                    dcc.DatePickerSingle(
                                        id='end-date',
                                        min_date_allowed=date(1995, 1, 1),
                                        max_date_allowed=datetime.now().date(),
                                        date=datetime.now().date(),
                                    )
                                ],
                                    style={"float": "right"}
                                )
                            ],
                            className="row flex"
                        ),
                        html.Div(
                            [
                                html.Div([
                                    html.P("Short Moving Average:"),
                                    dcc.Input(20, type="number",
                                              id="short_average", max=50)
                                ],
                                    style={"float": "left"}
                                ),
                                html.Div([
                                    html.P("Long Moving Average:"),
                                    dcc.Input(100, type="number",
                                              id="end_average", min=50)
                                ],
                                    style={"float": "right"}
                                )
                            ],
                            className="row flex"
                        ),
                        html.Div(
                            [
                                html.Div([
                                    html.P("Investment amount:"),
                                    dcc.Input(500, type="number",
                                              id="investment_amount")
                                ],
                                    style={"float": "left"}
                                ),
                                html.Div([
                                    html.P("End amount:"),
                                    dcc.Input("", type="text",
                                              id="end_amount", disabled=True)
                                ],
                                    style={"float": "right"}
                                ),
                            ],
                            className="row flex"
                        )
                    ],
                    className="pretty_container",
                ),
                # html.Div(
                #     html.P("You turned")
                # )
            ],
            className="four columns",
        ),
        html.Div(
            [
                html.Div(
                    [dcc.Graph(id="main_graph")],
                    id="main-graph-container",
                    className="pretty_container",
                ),
                html.Div(
                    [
                        html.H5(
                            "Transactions",
                            style={"text-align": "center"}
                        ),
                        dash_table.DataTable(
                            columns=[
                                {"name": "Buy Date", "id": "buy_date_col"},
                                {"name": "Buy Price", "id": "buy_price_col"},
                                {"name": "Sell Date", "id": "sell_date_col"},
                                {"name": "Sell Price", "id": "sell_price_col"},
                                {"name": "Percent", "id": "percent_col"},
                                {"name": "Margin", "id": "margin_col"},
                            ],
                            data=[

                            ],
                            style_cell={'fontSize': 14,
                                        'font-family': 'sans-serif'},
                            style_header={
                                'textAlign': 'center',
                                'fontWeight': 'bold',
                                'color': 'white',
                                'background-color': '#4d4d4d'
                            },
                            style_data={
                                'textAlign': 'center',
                                'color': 'white',
                                'background-color': '#4d4d4d'
                            },
                            style_data_conditional=[
                                {
                                    'if': {
                                        'filter_query': '{margin_col} > 0',
                                    },
                                    'backgroundColor': "#B3E6B5",
                                    'color': 'black'
                                },
                                {
                                    'if': {
                                        'filter_query': '{margin_col} < 0',
                                    },
                                    'backgroundColor': "#D99090",
                                    'color': 'black'
                                }
                            ],
                            id="dec_table"
                        ),
                    ],
                    className="pretty_container"
                )
            ],
            id="right-column",
            className="eight columns",
            style={"overflow-y": "auto", "maxHeight": "80vh"}
        ),
    ],
    className="row container-display",
)


@callback(
    [
        Output("main_graph", "figure"),
        Output("dec_table", "data"),
        Output("end_amount", "value")
    ],
    [
        Input('ticker-dropdown', 'value'),
        Input("start-date", "date"),
        Input("end-date", "date"),
        Input("short_average", "value"),
        Input("end_average", "value"),
        Input("investment_amount", "value")
    ]
)
def params_update(ticker, start_date, end_date, short_avg, long_avg, investment_amount):
    if not (ticker and start_date and end_date and short_avg and long_avg and investment_amount):
        raise PreventUpdate

    # get stock data
    data = get_data(ticker, start_date, end_date)
    # add the short and long moving averages (this moves start date to start date + long_avg)
    full_data = add_avgs(data, short_avg, long_avg)
    # find all of the intersections (this adds)
    intersections = find_intersections(full_data)
    # get the initial price from the data (this will be exactly at start date)
    initial_price = full_data['Close'].values[0]
    graph = multi_line_plot(ticker, full_data, intersections)
    # get the table for each transaction
    transactions_table = melt_intersections(
        intersections.index, full_data["Close"], investment_amount)

    # round for display
    table_data = [
        {
            "buy_date_col":     row["buy_date"].date(),
            "buy_price_col":    f"${np.round(row['buy_price'], 2)}",
            "sell_date_col":    row["sell_date"].date(),
            "sell_price_col":   f"${np.round(row['sell_price'], 2)}",
            "percent_col":      f"{np.round(100*    row['percent'], 2)}%",
            "margin_col":       np.round(row["margin"], 2),
        }
        for _, row in transactions_table.iterrows()
    ]

    end_amount = transactions_table['margin'].values.cumsum(
    )[-1].round(2) + investment_amount

    return [graph, table_data, f'{end_amount}']

    # TODO: melt the data table
