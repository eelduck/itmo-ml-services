import dash_bootstrap_components as dbc
from dash import dash_table, dcc, html

login_layout = html.Div(
    [
        dbc.Container(
            [
                dbc.Row(
                    [
                        dbc.Col(
                            dbc.Card(
                                [
                                    dbc.CardHeader("Login"),
                                    dbc.CardBody(
                                        [
                                            dbc.Row(
                                                [
                                                    dbc.Col(
                                                        dbc.Label("Email"), width=4
                                                    ),
                                                    dbc.Col(
                                                        dbc.Input(
                                                            id="login-email",
                                                            placeholder="Enter email",
                                                        ),
                                                        width=8,
                                                    ),
                                                ]
                                            ),
                                            dbc.Row(
                                                [
                                                    dbc.Col(
                                                        dbc.Label("Password"), width=4
                                                    ),
                                                    dbc.Col(
                                                        dbc.Input(
                                                            id="login-password",
                                                            placeholder="Enter password",
                                                            type="password",
                                                        ),
                                                        width=8,
                                                    ),
                                                ]
                                            ),
                                            dbc.Row(
                                                [
                                                    dbc.Col(
                                                        dbc.Button(
                                                            "Login",
                                                            id="login-button",
                                                            className="mt-3",
                                                            color="primary",
                                                        ),
                                                        width={"size": 6, "offset": 4},
                                                    ),
                                                ]
                                            ),
                                            html.Div(id="login-status"),
                                        ]
                                    ),
                                ]
                            ),
                            width=6,
                        )
                    ],
                    justify="center",
                )
            ]
        )
    ]
)

register_layout = html.Div(
    [
        dbc.Container(
            [
                dbc.Row(
                    [
                        dbc.Col(
                            dbc.Card(
                                [
                                    dbc.CardHeader("Register"),
                                    dbc.CardBody(
                                        [
                                            dbc.Row(
                                                [
                                                    dbc.Col(
                                                        dbc.Label("Email"), width=4
                                                    ),
                                                    dbc.Col(
                                                        dbc.Input(
                                                            id="register-email",
                                                            type="email",
                                                            placeholder="Enter email",
                                                        ),
                                                        width=8,
                                                    ),
                                                ]
                                            ),
                                            dbc.Row(
                                                [
                                                    dbc.Col(
                                                        dbc.Label("Password"), width=4
                                                    ),
                                                    dbc.Col(
                                                        dbc.Input(
                                                            id="register-password",
                                                            type="password",
                                                            placeholder="Enter password",
                                                        ),
                                                        width=8,
                                                    ),
                                                ]
                                            ),
                                            dbc.Row(
                                                [
                                                    dbc.Col(
                                                        dbc.Button(
                                                            "Register",
                                                            id="register-button",
                                                            className="mt-3",
                                                            color="primary",
                                                        ),
                                                        width={"size": 6, "offset": 4},
                                                    ),
                                                ]
                                            ),
                                            html.Div(id="registration-status"),
                                        ]
                                    ),
                                ]
                            ),
                            width=6,
                        )
                    ],
                    justify="center",
                )
            ]
        )
    ]
)


predictions_layout = dbc.Container(
    [
        dbc.Row(
            dbc.Col(
                html.Div(
                    [
                        html.Span(id="user-email-display"),
                        html.Span(" | Balance: "),
                        html.Span(id="user-balance-display"),
                    ],
                    style={"textAlign": "right", "marginBottom": "20px"},
                ),
                width={"size": 6, "offset": 3},
                className="d-flex justify-content-end align-items-center",
            ),
            className="mb-3",
        ),
        html.H3("Make a Prediction", className="text-center mb-5"),
        # Dropdown for model selection
        dbc.Row(
            [
                dbc.Col(dbc.Label("Select a Model:"), width={"size": 3, "offset": 3}),
                dbc.Col(
                    dcc.Dropdown(
                        id="model-dropdown",
                        options=[],  # The options will be populated by the callback
                        placeholder="Select a model",
                        style={"width": "100%", "textOverflow": "ellipsis"},
                    ),
                    width=6,
                ),
            ],
            className="mb-4",
        ),
        # File upload
        dbc.Row(
            [
                dbc.Col(dbc.Label("Upload CSV File:"), width={"size": 2, "offset": 3}),
                dbc.Col(
                    dcc.Upload(
                        id="upload-data",
                        children=html.Div(
                            ["Drag and Drop or ", html.A("Select Files")]
                        ),
                        style={
                            "width": "100%",
                            "height": "60px",
                            "lineHeight": "60px",
                            "borderWidth": "1px",
                            "borderStyle": "dashed",
                            "borderRadius": "5px",
                            "textAlign": "center",
                        },
                    ),
                    width=4,
                ),
            ],
            className="mb-4",
        ),
        # Predict button
        dbc.Row(
            dbc.Col(
                dbc.Button(
                    "Predict", id="predict-button", color="primary", className="mt-2"
                ),
                width={"size": 2, "offset": 5},
                className="mb-5",
            ),
        ),
        html.Div(id="output-data-upload", className="mb-5"),  # Placeholder for output
        html.H3("Your Predictions", className="text-center mb-3"),
        dbc.Button(
            "Get Predictions",
            id="get-predictions-button",
            color="primary",
            className="mb-4",
        ),
        html.Div(
            id="predictions-status", className="mb-3"
        ),  # Placeholder for any status messages
        dash_table.DataTable(
            id="predictions-table",
            columns=[
                {"name": i, "id": i}
                for i in ["model_id", "filename", "predictions", "created_at"]
            ],
            data=[],
            style_table={"height": "300px", "overflowY": "auto"},
        ),
    ],
    fluid=True,
    style={"maxWidth": "70%"},
)
