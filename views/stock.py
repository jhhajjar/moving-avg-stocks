import dash_bootstrap_components as dbc
import numpy as np
import pandas as pd
from dash.exceptions import PreventUpdate
from datetime import date, datetime
from utils import get_data, multi_line_plot, find_intersections, add_avgs, calc_percents, get_margins, process_end
from dash import Input, Output, State, callback, dcc, html, dash_table

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
                        html.P("Investment amount:"),
                        dcc.Input(350, type="number", id="investment_amount")
                    ],
                    className="pretty_container",
                ),
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
                                {"name": "Date", "id": "date_col"},
                                {"name": "Close Price", "id": "close_col"},
                                {"name": "Decision", "id": "decision_col"},
                                {"name": "Percent Difference", "id": "perc_col"},
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
                                        'column_id': 'perc_col'
                                    },
                                    'backgroundColor': "#B3E6B5",
                                    'color': 'black'
                                },
                                # ],
                                {
                                    'if': {
                                        'filter_query': '{margin_col} < 0',
                                        'column_id': 'perc_col'
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
    if not ticker:
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
    # get the margins for each transaction
    percs = calc_percents(initial_price, intersections)
    intersections['percs'] = percs
    intersections['margins'] = get_margins(investment_amount, intersections)
    # round for display
    # intersections.values = np.round(intersections.values, 2)
    table_data = [
        {
            "date_col": i.date(),
            "close_col":    f"${np.round(row['Close'], 2)}",
            "decision_col": row["decision"],
            "perc_col":     f'{np.round(row["percs"]* 100, 2)}%',
            "margin_col":   np.round(row["margins"], 2),
        }
        for i, row in intersections.iterrows()
    ]

    return [graph, table_data]
