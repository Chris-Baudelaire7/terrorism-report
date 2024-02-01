from dash import Input, Output, State, html, callback, no_update


@callback(
    Output("modal", "is_open"),
    Input("summury-country", "n_clicks"),
    State("modal", "is_open"),
)
def toggle_modal(n, is_open):
    if n:
        return not is_open
    return is_open
