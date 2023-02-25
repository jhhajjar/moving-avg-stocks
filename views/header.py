from dash import html, callback, Input, Output

header = html.Div(
    [
        html.Div(
            [
                html.A(
                    html.Img(
                        src=r'assets/Dataesg_logo.png',
                        id="plotly-image",
                        style={
                            "height": "40px",
                            "width": "auto",
                            "margin-bottom": "25px",
                        },
                    ),
                    href="https://dataesg.com/"
                ),
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
                    href="https://dataesg.com/contact-us",
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
