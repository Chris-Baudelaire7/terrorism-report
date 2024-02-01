import dash
from dash import html, dcc
import dash_mantine_components as dmc
import dash_bootstrap_components as dbc
from dash_iconify import DashIconify
from apps import header, thesis
from data_preparation import *
from graph_without_callback import *
from components import *


app_name = "comparative-analysis"

dash.register_page(
    __name__, path=f"/{app_name}", title=app_name, description=app_name, name=app_name)

layout = html.Div(id=app_name, className="container container-lg layout", children=[

    html.H1("Comparative Analysis", className="display-4"),

    html.Div(className="preambule mt-3", children=[
        dcc.Markdown(
            """
            Le Global Terrorism Index (GTI) est établi par L’Institute for Economics and Peace (IEP). L’Institute for Economics and Peace est un grand groupe international qui développe des indices afin d’évaluer et de mesurer la paix et la violence dans le monde. Dans cet objectif, depuis trois ans, il se concentre sur l’impact du terrorisme et a développé le GTI qui permet de quantifier le risque terroriste. Il s’agit d’un indice annuel pour chaque pays se présentant sous la forme d’une note allant de 0 pour les pays les moins affectés par le terrorisme, à 10 pour les pays les plus touchés. En 2015, le GTI a été évalué dans 162 pays à partir de la plus grande base de données recensant les actes terroristes : la GTD (présentée dans le chapitre 2). Les variables utilisées pour le calcul sont les suivantes :– Nombre total d’attaques sur l’année– Nombre de morts (nkill)

            """,

            className="preambule_text",
        )
    ]),
        
    html.Div(className="row justify-content-center mt-3", children=[

        html.Div(className="col-lg-4", children=[
            html.Span("Selectionner une métrique", className="text-white"),
            dcc.Dropdown(
                id="severity-metric-versus",
                options=[
                    {"label": x, "value": y}
                    for x, y in zip(["Incidence", "Décès", "Victimes (Blessés + Décès)"], ["size", "nkill", "casualties"])
                ],
                value="size",
                placeholder="Selection",
            )
        ]),

        html.Div(className="selection d-flex justify-content-center mt-3", children=[
            html.Small("Type de graphique:"),
            dmc.ChipGroup(value="bar", id="graph-type-versus", children=[
                dmc.Chip(x, value=y, size="sm", color="red")
                for x, y in zip(
                    ["Diagramme circulaire (repartition en %)",
                     "Evolution (relative) dans le temps"],
                    ["pie", "bar"]
                )
            ])
        ])

    ]),


    html.Div(className="row justify-content-center align-items-center mt-3", children=[

        html.Div(className="col-lg-6 carte", children=[
            dcc.Graph(id="pie-success", config=dict(displayModeBar=False))
        ]),

        html.Div(className="col-lg-6 carte", children=[
            dcc.Graph(id="pie-suicide", config=dict(displayModeBar=False))
        ]),

        html.Div(className="col-lg-6 carte", children=[
            dcc.Graph(id="pie-individual", config=dict(displayModeBar=False))
        ]),

        html.Div(className="col-lg-6 carte", children=[
            dcc.Graph(id="pie-crit", config=dict(displayModeBar=False))
        ]),

        html.Div(className="mt-3", children=[
            dcc.Markdown(
                "Bienvenue dans notre tableau de bord dédié à l'analyse des données relatives au terrorisme dans le monde. Ce tableau de bord a pour objectif de vous fournir une vue approfondie et dynamique de l'évolution des actes terroristes à travers le temps et l'espace. À travers une série de visualisations interactives et de données actualisées, nous explorerons les tendances, les régions les plus touchées, les groupes terroristes les plus actifs, et bien plus encore. Comprendre le terrorisme."
            ),
        ]),

    ]),


])
