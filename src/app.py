import dash
from flask import Flask
from dash import html, Dash
import dash_bootstrap_components as dbc

from apps import navbar

from callback.callback1 import *
from callback.callback2 import *
from callback.callback3 import *
from callback.callback4 import *
from callback.other_graph_callback import *
from callback.callback_special import *



# Parameters 

app_params = {
    "server": Flask(__name__),
    "title": "Le Terrorisme dans le monde - Analyse de données",
    "use_pages": True,
    "update_title": "Patientez un instant...",
    "url_base_pathname": "/",
    "external_stylesheets": [dbc.themes.CYBORG, dbc.icons.BOOTSTRAP],
    "suppress_callback_exceptions": True,
    "meta_tags": [{'name': 'viewport', 'content': 'width=device-width, initial-scale=1.0'}]
}

server_params = {
    "debug": False, 
}


# Create app

app = Dash(__name__, **app_params)

server = app.server

app.layout = html.Div(id="app-root", className="app-root", children=[
    
    navbar.navbar, 
        
    html.Div(id="pages", className="pages", children=[
        dash.page_container
    ]),
    
])


# Launch server app

if __name__ == '__main__':
    app.run_server(**server_params)