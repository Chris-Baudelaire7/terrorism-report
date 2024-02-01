import dash
from dash import html, dcc
import dash_mantine_components as dmc
import dash_bootstrap_components as dbc
from dash_iconify import DashIconify
from apps import header, thesis
from data_preparation import *
from graph_without_callback import *
from components import *

from callback.economic_imapct import *


app_name = "economic-impact"

dash.register_page(
    __name__, path=f"/{app_name}", title=app_name, description=app_name, name=app_name)

layout = html.Div(id=app_name, className="container container-lg layout", children=[

    html.H1("Economic Impact of Terrorist Activities", className="display-4"),

    html.Div(className="preambule mt-3", children=[
        dcc.Markdown(
            """
            Le Global Terrorism Index (GTI) est établi par L’Institute for Economics and Peace (IEP). L’Institute for Economics and Peace est un grand groupe international qui développe des indices afin d’évaluer et de mesurer la paix et la violence dans le monde. Dans cet objectif, depuis trois ans, il se concentre sur l’impact du terrorisme et a développé le GTI qui permet de quantifier le risque terroriste. Il s’agit d’un indice annuel pour chaque pays se présentant sous la forme d’une note allant de 0 pour les pays les moins affectés par le terrorisme, à 10 pour les pays les plus touchés. En 2015, le GTI a été évalué dans 162 pays à partir de la plus grande base de données recensant les actes terroristes : la GTD (présentée dans le chapitre 2). Les variables utilisées pour le calcul sont les suivantes :– Nombre total d’attaques sur l’année– Nombre de morts (nkill)

            """,

            className="preambule_text",
        )
    ]),

    html.Div(className="row mb-3", children=[

        dcc.Markdown(
            "Dans l'ensemble, le nombre d'attaques terroristes dans le monde a augmenté de manière significative au fildes décennies. Cette augmentation peut être attribuée à plusieurs facteurs, notamment la montée de groupesterroristes, la facilité accrue de communication et de recrutement grâce à Internet, ainsi que les conflitsrégionaux et internationaux. Au cours de cette période, des groupes terroristes tels qu'Al-Qaïda et l'Étatislamique (ISIS) sont devenus des acteurs mondiaux majeurs du terrorisme, lançant des attaques à l'échelleinternationale et inspirant des cellules terroristes dans de nombreux pays.",

            className="preambule_text",
        ),

    ]),

    html.Div(className="row align-items-center mt-5", children=[

        html.Div(className="col-12 carte", children=[
             html.Div(id="series-damages"),
             
             html.Div(className="selection d-flex justify-content-center mt-2", children=[
                 dmc.ChipGroup(value="1", id="select-property", children=[
                     dmc.Chip(x, value=y, size="sm", color="red")
                     for x, y in zip(
                         ["Ayant causé des dégâts matériels",
                          "Sans dégâts matériels"],
                         ["1", "0"]
                     )
                 ]),
             ])
        ])

    ]),
    
    

    html.Div(className="row mt-3", children=[

        dcc.Markdown(
             "Dans l'ensemble, le nombre d'attaques terroristes dans le monde a augmenté de manière significative au fildes décennies. Cette augmentation peut être attribuée à plusieurs facteurs, notamment la montée de groupesterroristes, la facilité accrue de communication et de recrutement grâce à Internet, ainsi que les conflitsrégionaux et internationaux. Au cours de cette période, des groupes terroristes tels qu'Al-Qaïda et l'Étatislamique (ISIS) sont devenus des acteurs mondiaux majeurs du terrorisme, lançant des attaques à l'échelleinternationale et inspirant des cellules terroristes dans de nombreux pays.",

             className="preambule_text",
             ),

    ]),


    html.Div(className="row align-items-center mt-5 pt-5", children=[

        html.Div(className="col-lg-6 carte", children=[
            html.Div(id="repartition-damages")
        ]),

        html.Div(className="col-lg-6 carte", children=[
            html.Div(id="repartition-dollars")
        ]),

    ]),

    html.Div(className="row justify-content-center align-items-center mt-3", children=[
        html.Div(className="col", children=[
             dcc.Markdown(
                 "Bienvenue dans notre tableau de bord dédié à l'analyse des données relatives au terrorisme dans le monde. Ce tableau de bord a pour objectif de vous fournir une vue approfondie et dynamique de l'évolution des actes terroristes à travers le temps et l'espace. À travers une série de visualisations interactives et de données actualisées, nous explorerons les tendances, les régions les plus touchées, les groupes terroristes les plus actifs, et bien plus encore. Comprendre le terrorisme."
             ),
             ]),

    ]),


    html.Div(className="row justify-content-center align-items-center mt-5 pt-5", children=[

        html.Div(className="col-lg-4", children=[
             html.Div(className="row mb-3", children=[
                 html.Div(className="col", children=[
                     html.Span("Cause", className=""),
                     dcc.Dropdown(
                         id="choose-category",
                         options=[
                            {"label": x, "value": y}
                            for x, y in zip(["Groupe terroriste", "Mode d'attaque", "Type d'arme", "Cible visées"], ["gname", "attacktype", "weaptype1", "targtype"])
                         ],
                         value="gname",
                         placeholder="Selection",
                     )
                 ]),

                 html.Div(className="col", children=[
                     html.Span("Groupe terroriste", className="d-block"),
                     dcc.Dropdown(
                         id="cost",
                         options=[
                            {"label": x, "value": x} for x in list(df["propextent_txt"].unique())[1:-1]
                         ],
                         value=list(df["propextent_txt"].unique())[1:-1][0],
                         placeholder="Selection",
                     ),
                 ]),
             ]),

             dcc.Markdown(
                 "Bienvenue dans notre tableau de bord dédié à l'analyse des données relatives au terrorisme dans le monde. Ce tableau de bord a pour objectif de vous fournir une vue approfondie et dynamique de l'évolution des actes terroristes à travers le temps et l'espace. À travers une série de visualisations interactives et de données actualisées, nous explorerons les tendances, les régions les plus touchées, les groupes terroristes les plus actifs, et bien plus encore. Comprendre le terrorisme."
             ),
             ]),

        html.Div(className="col-lg-8 carte", children=[
            dcc.Graph(id="number-attack-with-damage-by-category",
                      config=dict(displayModeBar=False))
        ]),

    ]),


    html.Div(className="row justify-content-center align-items-center mt-5", children=[

        html.Div(className="col-lg-12", children=[
            html.H4(
                "Carte graphique: repatition des attaque par coût (en dollars $)"),
            dcc.Markdown(
                "Bienvenue dans notre tableau de bord dédié à l'analyse des données relatives au terrorisme dans le monde. Ce tableau de bord a pour objectif de vous fournir une vue approfondie et dynamique de l'évolution des actes terroristes à travers le temps et l'espace. À travers une série de visualisations interactives et de données actualisées, nous explorerons les tendances, les régions les plus touchées, les groupes terroristes les plus actifs, et bien plus encore. Comprendre le terrorisme."
            ),
        ]),

    ]),



    html.Div(className="row justify-content-center align-items-center mt-5 pt-5", children=[

        html.Div(className="col-lg-8 carte", children=relationship()),

        html.Div(className="col-lg-4", children=[
            dcc.Markdown(
                "Bienvenue dans notre tableau de bord dédié à l'analyse des données relatives au terrorisme dans le monde. Ce tableau de bord a pour objectif de vous fournir une vue approfondie et dynamique de l'évolution des actes terroristes à travers le temps et l'espace. À travers une série de visualisations interactives et de données actualisées, nous explorerons les tendances, les régions les plus touchées, les groupes terroristes les plus actifs, et bien plus encore. Comprendre le terrorisme."
            ),
        ]),

    ]),


    


])
