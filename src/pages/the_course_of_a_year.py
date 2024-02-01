import dash
import dash_echarts
from dash import html, dcc
import dash_mantine_components as dmc
import dash_bootstrap_components as dbc
from data_preparation import *
from graph_without_callback import *
from components import *

from callback.the_course_of_a_year import *


app_name = "the-course-of-a-year"

dash.register_page(__name__, path=f"/{app_name}", title=app_name, description=app_name, name=app_name)


layout = html.Div(id=app_name, className="container container-lg layout", children=[
    
    html.H1("Analyse année par année"),
    dcc.Markdown(
                """
                Nous utilison une moyenne quinquennale (sur une période de 5 ans) pour analyser les tendances à long terme dans les données temporelles des acivités terroristes, en réduisant le bruit et en fournissant une vue d'ensemble plus claire des évolutions sur plusieurs années.
                
                On constate que les activités terroristes et leurs conséquences connaissent un fort accroissement à partir des années 2005 à 2017. Cette augmentation peut être attribuée à plusieurs facteurs, notamment la montée de groupes terroristes, la facilité accrue de communication et de recrutement grâce à Internet, ainsi que les conflits régionaux et internationaux
                """,
                                        
                className="preambule_text",
            ),
        
    
    html.Div(className="row", children=[

        html.Div(className="title-section mb-3", children=[
            html.Div(className="dash"),
            html.H2("Tendances Terroriste Au Cours D'une Année", className="")
        ]),

        dcc.Markdown(
            "Dans l'ensemble, le nombre d'attaques terroristes dans le monde a augmenté de manière significative au fildes décennies. Cette augmentation peut être attribuée à plusieurs facteurs, notamment la montée de groupesterroristes, la facilité accrue de communication et de recrutement grâce à Internet, ainsi que les conflitsrégionaux et internationaux. Au cours de cette période, des groupes terroristes tels qu'Al-Qaïda et l'Étatislamique (ISIS) sont devenus des acteurs mondiaux majeurs du terrorisme, lançant des attaques à l'échelleinternationale et inspirant des cellules terroristes dans de nombreux pays.",

            className="preambule_text",
        ),

    ]),
    
    
    html.Div(className="row align-items-center mt-5", children=[

        html.Div(className="col-lg-7", children=[
            dcc.Loading(dcc.Graph(id="period-timeseries",
                        config=dict(displayModeBar=False)),)
        ]),

        html.Div(className="col-lg-5", children=[
            dcc.Loading(dcc.Graph(id="period-distribution",
                        config=dict(displayModeBar=False)))
        ])

    ]),
    
    
    html.Div(className="row justify-content-center align-items-center mt-5 ", children=[

        html.Div(className="col-lg-8", children=[

            dcc.Loading(dcc.Graph(config=dict(displayModeBar=False),
                        id="mean-day"), color="red")
        ]),

        html.Div(className="col-lg-4", children=[
            html.Div(className="mb-2", children=[
                html.P("Année"),
                dcc.Slider(1970, 2020, 1, value=2002, marks=None, included=False, id="slider",
                           tooltip={"placement": "bottom",
                                    "always_visible": True}
                           ),
            ]),
            dcc.Markdown(
                "Bienvenue dans notre tableau de bord dédié à l'analyse des données relatives au terrorisme dans le monde. Ce tableau de bord a pour objectif de vous fournir une vue approfondie et dynamique de l'évolution des actes terroristes à travers le temps et l'espace. À travers une série de visualisations interactives et de données actualisées, nous explorerons les tendances, les régions les plus touchées, les groupes terroristes les plus actifs, et bien plus encore. Comprendre le terrorisme."
            ),
        ]),

    ]),
    
    
    html.Div(className="row align-items-center mt-5", children=[
        
        html.Div(className="col-lg-5", children=[
            #dcc.Loading(dcc.Graph(id="month-timeseries", config=dict(displayModeBar=False)),),
            
            html.Div(id="echarts")
        ]),
        
        html.Div(className="col-lg-7", children=[
            dbc.Tabs(class_name="tabular", children=[
                dbc.Tab(
                    label="Repartition en pourcentage", 
                    tab_style=tab_style,
                    active_tab_style=active_tab_style,
                    children=[
                        html.Div(className="mt-3", children=[
                            dcc.Loading(dcc.Graph(id="repartition-in-percent-by-month", config=dict(displayModeBar=False))),
            
                            html.Div(className="selection d-flex justify-content-center mt-2", children=[
                                dmc.ChipGroup(value="attacktype", id="select-category", children=[
                                    dmc.Chip(x, value=y, size="sm", color="red") 
                                    for x, y in zip(
                                        ["Par type d'attaque", "Par armes utilisées", "Par cible visée"], 
                                        ["attacktype", "weaptype1", "targtype"]
                                    )
                                ])

                            ])
                        ])
                    ]
                ),
                
                dbc.Tab(
                    label="Evolution temporelle absolue/relative",
                    active_tab_style=active_tab_style,
                    class_name="bg-danger",
                    children=[
                        html.Div(className="mt-3", children=[
                            dcc.Loading(
                                dcc.Graph(id="serie-relative-absolue", config=dict(displayModeBar=False))),

                            html.Div(className="selection d-flex justify-content-center mt-2", children=[
                                dmc.ChipGroup(value="attacktype", id="slct-category", children=[
                                    dmc.Chip(
                                        x, value=y, size="sm", color="red")
                                    for x, y in zip(
                                        ["Par type d'attaque",
                                            "Par armes utilisées", "Par cible visée"],
                                        ["attacktype", "weaptype1", "targtype"]
                                    )
                                ])

                            ])

                        ])
                    ]
                ),
            ])
        ])

    ]),
    
    
    html.Div(className="row mt-3", children=[

        dcc.Markdown(
            "Dans l'ensemble, le nombre d'attaques terroristes dans le monde a augmenté de manière significative au fildes décennies. Cette augmentation peut être attribuée à plusieurs facteurs, notamment la montée de groupesterroristes, la facilité accrue de communication et de recrutement grâce à Internet, ainsi que les conflitsrégionaux et internationaux. Au cours de cette période, des groupes terroristes tels qu'Al-Qaïda et l'Étatislamique (ISIS) sont devenus des acteurs mondiaux majeurs du terrorisme, lançant des attaques à l'échelleinternationale et inspirant des cellules terroristes dans de nombreux pays.",

            className="preambule_text",
        )

    ])
    
])

