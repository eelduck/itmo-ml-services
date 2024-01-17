import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import requests
from dash import callback_context
from dash.dependencies import Input, Output

app = dash.Dash(
    __name__,
    external_stylesheets=[dbc.themes.BOOTSTRAP],
    suppress_callback_exceptions=True,
)

app.layout = html.Div(
    [
        dbc.Container(
            [
                dbc.Row(
                    [dbc.Col(html.H2("Welcome to Our App", className="text-center"))]
                ),
                dbc.Row(
                    [
                        dbc.Col(
                            dbc.Card(
                                [
                                    dbc.CardBody(
                                        [
                                            dcc.Location(id="url", refresh=True),
                                            html.Div(id="page-content"),
                                        ]
                                    )
                                ]
                            )
                        )
                    ]
                ),
            ]
        )
    ]
)

# Define the layout for the login page
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

# Define the layout for the registration page
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
                                                        dbc.Label("Username"), width=4
                                                    ),
                                                    dbc.Col(
                                                        dbc.Input(
                                                            id="register-username",
                                                            placeholder="Enter username",
                                                        ),
                                                        width=8,
                                                    ),
                                                ]
                                            ),
                                            dbc.Row(
                                                [
                                                    dbc.Col(
                                                        dbc.Label("Email"), width=4
                                                    ),
                                                    dbc.Col(
                                                        dbc.Input(
                                                            id="register-email",
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
                                                            "Register",
                                                            id="register-button",
                                                            className="mt-3",
                                                            color="primary",
                                                        ),
                                                        width={"size": 6, "offset": 4},
                                                    ),
                                                ]
                                            ),
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

# Layout for the predictions page
predictions_layout = html.Div(
    [html.H3("Predictions Page"), html.P("Prediction page content goes here.")]
)


@app.callback(
    Output("login-status", "children"),
    Input("login-button", "n_clicks"),
    [Input("login-email", "value"), Input("login-password", "value")],
    prevent_initial_call=True,
)
def login_user(n_clicks, email, password):
    if n_clicks is None:
        return dash.no_update

    if not email or not password:
        return "Please fill out all fields."

    # Check what triggered the callback
    ctx = callback_context
    if not ctx.triggered or ctx.triggered[0]["prop_id"].split(".")[0] != "login-button":
        return ""

    login_data = {"username": email, "password": password}

    try:
        response = requests.post(
            "http://localhost:8000/auth/jwt/login/", data=login_data
        )

        if response.status_code == 200:
            # Assuming the JWT token is returned in the response
            # Set the received JWT token in a cookie
            # Note: Dash does not directly support setting cookies in the client. This requires a workaround.
            return "/predictions"
        else:
            return f"Login failed: {response.text}"

    except requests.exceptions.RequestException as e:
        return f"An error occurred: {e}"


# Callback to switch between login and registration page
app.layout = html.Div(
    [dcc.Location(id="url", refresh=False), html.Div(id="page-content")]
)


@app.callback(Output("page-content", "children"), [Input("url", "pathname")])
def display_page(pathname):
    if pathname == "/login":
        return login_layout
    elif pathname == "/register":
        return register_layout
    elif pathname == "/predictions":
        return predictions_layout
    else:
        return "404 Page Not Found"


if __name__ == "__main__":
    app.run_server(debug=True)
