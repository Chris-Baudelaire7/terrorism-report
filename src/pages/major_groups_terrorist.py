import dash
from dash import html, dcc
import dash_mantine_components as dmc
import dash_bootstrap_components as dbc
from dash_iconify import DashIconify
from apps import header, thesis
from data_preparation import *
from graph_without_callback import *
from components import *

# https://www.janes.com/osint-capabilities/military-threat-intelligence/terrorism-and-insurgency


app_name = "major-terrorist-groups"

dash.register_page(__name__, path=f"/{app_name}", title=app_name, description=app_name, name=app_name)

layout = html.Div(id=app_name, className="container container-lg layout", children=[
        
    
    html.H1("Major Terrorist Groups", className="display-4"),
    
    html.Div(className="preambule", children=[
        dcc.Markdown(
            "Bienvenue dans notre tableau de bord dédié à l'analyse des données relatives au terrorisme dans le monde. Ce tableau de bord a pour objectif de vous fournir une vue approfondie et dynamique de l'évolution des actes terroristes à travers le temps et l'espace. À travers une série de visualisations interactives et de données actualisées, nous explorerons les tendances, les régions les plus touchées, les groupes terroristes les plus actifs, et bien plus encore. Comprendre le terrorisme nécessite une définition claire et une analyse précise, et c'est précisément ce que nous nous efforçons de vous offrir ici. Préparez-vous à plonger dans l'univers complexe et évolutif du terrorisme, en utilisant les données pour mieux comprendre ce phénomène mondial.",
                                    
            className="preambule_text",
        )
    ]),
        
    
    html.Div(className="row g-4 align-items-center mt-5", children=[

        html.Div(className="col-lg-4", children=[

            dcc.Markdown(
                "Dans l'ensemble, le nombre d'attaques terroristes dans le monde a augmenté de manière significative au fildes décennies. Cette augmentation peut être attribuée à plusieurs facteurs, notamment la montée de groupesterroristes, la facilité accrue de communication et de recrutement grâce à Internet, ainsi que les conflitsrégionaux et internationaux. Au cours de cette période, des groupes terroristes tels qu'Al-Qaïda et l'Étatislamique (ISIS) sont devenus des acteurs mondiaux majeurs du terrorisme, lançant des attaques à l'échelleinternationale et inspirant des cellules terroristes dans de nombreux pays.",

                className="preambule_text",
            ),

        ]),


        html.Div(className="col-lg-8 carte", children=[
            dcc.Loading(dcc.Graph(id="country-timeseries",
                        config=dict(displayModeBar=False))),
            choice_serie_type('choice_serie_type_countries')
        ])

    ]),
    
    
    html.Div(className="row align-items-center", children=[

        html.Div(className="col-lg-4", children=[
            html.Div(className="", children=[
                html.Span("Zone géographique", className=""),
                dcc.Dropdown(
                    id="selection",
                    options=[
                        {"label": x, "value": y}
                        for x, y in zip(["Continent", "Region", "Pays", "Province/État", "Ville"], ["continent", "region", "country", "provstate", "city"])
                    ],
                    value="region",
                    placeholder="Selection",
                )
            ]),

            dcc.Markdown(
                """
                Nous utilison une moyenne quinquennale (sur une période de 5 ans) pour analyser les tendances à long terme dans les données temporelles des acivités terroristes, en réduisant le bruit et en fournissant une vue d'ensemble plus claire des évolutions sur plusieurs années.
                
                On constate que les activités terroristes et leurs conséquences connaissent un fort accroissement à partir des années 2005 à 2017. Cette augmentation peut être attribuée à plusieurs facteurs, notamment la montée de groupes terroristes, la facilité accrue de communication et de recrutement grâce à Internet, ainsi que les conflits régionaux et internationaux
                """,

                className="preambule_text",
            )
        ]),

        html.Div(className="col-lg-8 carte", children=[
            dcc.Graph(config=dict(displayModeBar=False), id="sankey-graph")
        ]),

    ]),
    
])

