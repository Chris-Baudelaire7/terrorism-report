import dash
from flask import Flask
from dash import html, Dash
import dash_bootstrap_components as dbc
import dash_admin_components as dac
import dash_mantine_components as dmc
from apps import navbar

from callback.callback1 import *
from callback.callback2 import *
from callback.callback3 import *
from callback.callback4 import *
from callback.other_graph_callback import *
from callback.callback_special import *
from components import *



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
    "debug": True, 
    "port":27770,
}


# Create app

app = Dash(__name__, **app_params)

server = app.server

app.layout = dac.Page(id="app-root", className="app-root", children=[

    dmc.NotificationsProvider([


        navbar, sidebar, controlbar,

        html.Div(id="notifications-container"),

        dac.Body(className="page bg-white", children=[
            dash.page_container
        ]),

       # footer,

    ]),
    
    html.Script(src="echarts.js"),
    html.Script(src="theme/vintage.js")

])


# Launch server app

if __name__ == '__main__':
    app.run_server(**server_params)