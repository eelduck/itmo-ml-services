import dash
import dash_bootstrap_components as dbc
from callbacks.models import update_model_dropdown
from callbacks.predictions import get_predictions, predict
from callbacks.users import login_user, register_user, update_user_info
from dash import dcc, html
from dash.dependencies import Input, Output, State
from layouts import login_layout, predictions_layout, register_layout

app = dash.Dash(
    __name__,
    external_stylesheets=[dbc.themes.BOOTSTRAP],
    suppress_callback_exceptions=True,
)

app.layout = html.Div(
    [
        dcc.Location(id="url", refresh=False),
        html.Div(id="page-content"),
        dcc.Store(id="session", storage_type="session"),
    ]
)


@app.callback(
    [Output("page-content", "children")],
    [Input("url", "pathname")],
)
def display_page(pathname):
    print("Display Page Called with pathname:", pathname)
    if pathname == "/login":
        return [login_layout]
    elif pathname == "/register":
        return [register_layout]
    elif pathname == "/predictions":
        print("Returning Predictions Layout")
        return [predictions_layout]
    else:
        return ["404 Page Not Found"]


app.callback(
    [
        Output("user-email-display", "children"),
        Output("user-balance-display", "children"),
    ],
    [Input("url", "pathname")],
    [State("session", "data")],
)(update_user_info)

app.callback(
    [
        Output("login-status", "children"),
        Output("url", "pathname"),
        Output("session", "data"),
    ],
    [Input("login-button", "n_clicks")],
    [State("login-email", "value"), State("login-password", "value")],
    prevent_initial_call=True,
)(login_user)

app.callback(
    Output("registration-status", "children"),
    [Input("register-button", "n_clicks")],
    [State("register-email", "value"), State("register-password", "value")],
    prevent_initial_call=True,
)(register_user)

app.callback(
    [Output("predictions-table", "data"), Output("predictions-status", "children")],
    [Input("get-predictions-button", "n_clicks")],
    [State("session", "data")],
    prevent_initial_call=True,
)(get_predictions)

app.callback(Output("model-dropdown", "options"), [Input("url", "pathname")])(
    update_model_dropdown
)

app.callback(
    Output("output-data-upload", "children"),
    [Input("predict-button", "n_clicks")],
    [
        State("model-dropdown", "value"),
        State("upload-data", "contents"),
        State("upload-data", "filename"),
        State("session", "data"),
    ],
)(predict)

if __name__ == "__main__":
    app.run_server(host="0.0.0.0")
