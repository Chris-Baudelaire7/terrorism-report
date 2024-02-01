import dash
from dash import html, dcc
from dash_iconify import DashIconify
import dash_mantine_components as dmc
import dash_bootstrap_components as dbc

from callback.country_analysis import *
from callback.callback_components import *


app_name = "situation-by-country"

dash.register_page(__name__, path=f"/{app_name}", title=app_name, description=app_name, name=app_name)

modal = html.Div(children=[
    dbc.Modal(id="modal", is_open=False, scrollable=True, centered=True, backdrop=True, children=[
        dbc.ModalHeader(dbc.ModalTitle(
            "All Countries & Territories (By victims)", className="text-danger")),
            dbc.ModalBody(children=[
                """This is the content of timport dash
from dash import html, dcc
from dash_iconify import DashIconify
import dash_mantine_components as dmc
import dash_bootstrap_components as dbc

from callback.country_analysis import *
from callback.callback_components import *import dash
from dash import html, dcc
from dash_iconify import DashIconify
import dash_mantine_components as dmc
import dash_bootstrap_components as dbc

from callback.country_analysis import *
from callback.callback_components import *import dash
from dash import html, dcc
from dash_iconify import DashIconify
import dash_mantine_components as dmc
import dash_bootstrap_components as dbc

from callback.country_analysis import *
from callback.callback_components import *import dash
from dash import html, dcc
from dash_iconify import DashIconify
import dash_mantine_components as dmc
import dash_bootstrap_components as dbc

from callback.country_analysis import *
from callback.callback_components import *import dash
from dash import html, dcc
from dash_iconify import DashIconify
import dash_mantine_components as dmc
import dash_bootstrap_components as dbc

from callback.country_analysis import *
from callback.callback_components import *import dash
from dash import html, dcc
from dash_iconify import DashIconify
import dash_mantine_components as dmc
import dash_bootstrap_components as dbc

from callback.country_analysis import *
from callback.callback_components import *import dash
from dash import html, dcc
from dash_iconify import DashIconify
import dash_mantine_components as dmc
import dash_bootstrap_components as dbc

from callback.country_analysis import *
from callback.callback_components import *import dash
from dash import html, dcc
from dash_iconify import DashIconify
import dash_mantine_components as dmc
import dash_bootstrap_components as dbc

from callback.country_analysis import *
from callback.callback_components import *import dash
from dash import html, dcc
from dash_iconify import DashIconify
import dash_mantine_components as dmc
import dash_bootstrap_components as dbc

from callback.country_analysis import *
from callback.callback_components import *import dash
from dash import html, dcc
from dash_iconify import DashIconify
import dash_mantine_components as dmc
import dash_bootstrap_components as dbc

from callback.country_analysis import *
from callback.callback_components import *import dash
from dash import html, dcc
from dash_iconify import DashIconify
import dash_mantine_components as dmc
import dash_bootstrap_components as dbc

from callback.country_analysis import *
from callback.callback_components import *import dash
from dash import html, dcc
from dash_iconify import DashIconify
import dash_mantine_components as dmc
import dash_bootstrap_components as dbc

from callback.country_analysis import *
from callback.callback_components import *import dash
from dash import html, dcc
from dash_iconify import DashIconify
import dash_mantine_components as dmc
import dash_bootstrap_components as dbc

from callback.country_analysis import *
from callback.callback_components import *he modal"""
            ])
    ])
])



layout = html.Div(id=app_name, className="container-fluid layout", children=[
    
    modal,
    
    html.Div(className="d-flex justify-content-around align-items-center mb-3", children=[
        
        html.Div(className="text-center", children=[
            dmc.ActionIcon(
                DashIconify(icon="uim:graph-bar", width=170), 
                id="summury-country",
                variant="transparent",
                n_clicks=0
            )
        ]),
        
        html.Div(className="text-center", children=[
            html.Span("Terrorism Explorer", className="display-5 "),
            html.Br(),
            html.Span(
                "Click on a country or territory to see cases analysis and characteristics", 
                className="fs-5 "
            )
        ]),
        
        html.Div(className="text-center", children=[
            dmc.ActionIcon(
                DashIconify(icon="tabler:search", width=170,), variant="transparent",
            )
        ]),
        
    ]),
    
    html.Div(className="", children=[
        dcc.Graph(
            figure=choropleth(),
            id="choropleth",
            config=dict(displayModeBar=False),
            style={"width": "100%", "height": "100%"}
        ),
        dcc.Interval(id='choropleth-interval', interval=0.00000000005),
    ]),
    
    html.Div(className="mt-3 text-center", children=[
        html.Span("CASES: ", className="fw-bold"),
        html.Span("234567:", className="text-primary fw-bold"),
        
        html.Span("•", className="mx-2"),
        
        html.Span("DEATHS: ", className="fw-bold"),
        html.Span("234567:", className="text-danger fw-bold"),
        
        html.Span("•", className="mx-2"),
        
        html.Span("INJURED: ", className="fw-bold"),
        html.Span("234567:", className="text-warning fw-bold"),
        
        html.Span("•", className="mx-2"),
        
        html.Span("MOST ACTIVE: ", className="fw-bold"),
        html.Span("234567:", className="text-success fw-bold"),
        
        html.Span("•", className="mx-2"),
        
        html.Span("INJURED: ", className="fw-bold"),
        html.Span("234567:", className=""),
        
        html.Span("•", className="mx-2"),
        
        html.Span("INJURED: ", className="fw-bold"),
        html.Span("234567:", className="text-info fw-bold"),
        
        
    ]),
    
])

