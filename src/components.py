import dash
from dash import html, dcc
import dash_mantine_components as dmc
import dash_bootstrap_components as dbc
from dash_iconify import DashIconify
from apps import header, thesis
from data_preparation import *
from graph_without_callback import *
from data_preparation import *
from utils import *

def dropdown_geo(id):
    return html.Div(className="row justify-content-center", children=[
            
            html.Div(className="col-lg-4", children=[
                html.Span("Selectionner une zone géographique", className="text-white"),
                dcc.Dropdown(
                    id=id,
                    options=[{"label":"Monde", "value":"Monde"}]+
                                    
                            [{"label":"Par continent------------------------------", "disabled": True, "value":"Monde"}]+
                                                
                            [{"label": html.Span([x], style={'color': 'rgb(252,187,161)'}), "value": x,} 
                            for x in sorted(list(df.continent.unique()))]+
                                                
                            [{"label":"Par region---------------------------------", "disabled": True, "value":"Monde"}]+
                                                
                            [{"label": html.Span([y], style={'color': 'rgb(254,224,210'}),"value": y}
                            for y in sorted(list(df.region.unique()))],
                                                
                    value="Monde",
                    placeholder="Selection",
                    searchable=True,
                    clearable=True,
                    style={"color": "white"}
                )
            ])
        
        ])
    
    
def choice_serie_type(id):
    return html.Div(className="selection d-flex justify-content-center mt-2", children=[
                dmc.ChipGroup(value="relative", id=id, children=[
                    dmc.Chip(x, value=y, size="sm", color="red") 
                    for x, y in zip(
                        ["Série relative (zone)", "Série relative (bar)", "Série absolue"], 
                        ["relative", "relative-bar", "absolue"]
                    )
                ]),
            ])
    
    