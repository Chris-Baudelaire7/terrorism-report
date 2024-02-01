import dash
from dash import html, dcc
import dash_mantine_components as dmc
import dash_bootstrap_components as dbc
from dash_iconify import DashIconify
from apps import header, thesis
from data_preparation import *
from graph_without_callback import *
from components import *


app_name = "high-level-trends"

dash.register_page(__name__, path=f"/{app_name}", title=app_name, description=app_name, name=app_name)

active_tab_style = {
    "font-family": "serif",
    "border-bottom": "none"
}

tab_style={"marginLeft": "auto"}


layout = html.Div(id=app_name, className="layout", children=[
    
        
    # dmc.Affix(position={"bottom": 20, "left": 15}, className="affix", children=[
    #     # dmc.Button("I'm in an Affix Component", className="btn-danger"),
    #     html.Div(className="affix-graph", children=[
    #         dcc.Loading(dcc.Graph(id="geo-map_"), color="red", type="dot"),
    #     ])
    # ]),
    
    
    
    html.Div(className="row align-items-center", children=[
                
        html.H1("High Level Trends", className="display-4"),
        
        html.Div(className="mb-3", children=[
            dcc.Markdown(
                "Bienvenue dans notre tableau de bord dédié à l'analyse des données relatives au terrorisme dans le monde. Ce tableau de bord a pour objectif de vous fournir une vue approfondie et dynamique de l'évolution des actes terroristes à travers le temps et l'espace. À travers une série de visualisations interactives et de données actualisées, nous explorerons les tendances, les régions les plus touchées, les groupes terroristes les plus actifs, et bien plus encore. Comprendre le terrorisme."
            ),
        ]),
        
    ]),
    
    html.Div(className="row align-items-center", children=[
        
        html.Div(className="col-lg-12", children=[
            html.Div(className="row", children=[
                
                html.Div(className="", children=[
                    html.Span("Selectionner la cause", className=""),
                    dcc.Dropdown(
                        id="dropdown-cause-repartition",
                        options=[
                            {"label": x, "value": y} 
                            for x, y in zip(["Nombre d'incidences", "Nombre de blessés", "Nombre de décès"], ["size", "nwound", "nkill"])
                        ],
                        value="size",
                        placeholder="Selection",
                    )
                ]),
                
                html.Div(className="selection d-flex justify-content-center mt-3", children=[
                    html.Small("Type de graphique:"),
                    dmc.ChipGroup(value="pie", id="graph-type", children=[
                        dmc.Chip(x, value=y, size="sm", color="red") 
                        for x, y in zip(
                            ["Diagramme circulaire (repartition en %)", "Graphique à barre (classement)"], 
                            ["pie", "bar"]
                        )
                    ]),
                ]),
                html.Div(className="col-12 col-md-6 col-lg-6 carte", children=[
                    dcc.Loading(dcc.Graph(id="pie-group", config=dict(displayModeBar=False)), type="circle")
                ]),
                
                html.Div(className="col-12 col-md-6 col-lg-6 carte", children=[
                    dcc.Loading(dcc.Graph(id="pie-weapon", config=dict(displayModeBar=False)), type="circle")
                ]),
                
                html.Div(className="col-12 col-md-6 col-lg-6 carte", children=[
                    dcc.Loading(dcc.Graph(id="pie-attack", config=dict(displayModeBar=False)), type="circle")
                ]),
                
                html.Div(className="col-12 col-md-6 col-lg-6 carte", children=[
                    dcc.Loading(dcc.Graph(id="pie-target", config=dict(displayModeBar=False)), type="circle")
                ])
            ]),
        ]),
        
        html.Div(className="col-12", children=[
            dcc.Markdown(
                "Bienvenue dans notre tableau de bord dédié à l'analyse des données relatives au terrorisme dans le monde. Ce tableau de bord a pour objectif de vous fournir une vue approfondie et dynamique de l'évolution des actes terroristes à travers le temps et l'espace. À travers une série de visualisations interactives et de données actualisées, nous explorerons les tendances, les régions les plus touchées, les groupes terroristes les plus actifs, et bien plus encore. Comprendre le terrorisme."
            )
        ])
        
    ])
    
])


