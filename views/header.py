from dash import html, callback, Input, Output

header = html.Div(
    [
        html.Div(
            [
            ],
            className="one-third column",
        ),
        html.Div(
            [
                html.Div(
                    [
                        html.H3(
                            "Financial What If's",
                            style={"margin-bottom": "0px"},
                            id="title-text"
                        ),
                        html.H5(
                            "", style={"margin-top": "0px"},
                        ),
                    ],
                    className="on_black",
                )
            ],
            className="one-half column",
            id="title",
        ),
        html.Div(
            [
                html.A(
                    html.Button("Learn More", id="learn-more-button"),
                    href="https://www.investopedia.com/articles/active-trading/052014/how-use-moving-average-buy-stocks.asp",
                )
            ],
            className="one-third column",
            id="button"
        ),
    ],
    id="header",
    className="row flex-display",
    style={"margin-bottom": "25px"},
)
