import dash
from dash import html, dcc
import dash_mantine_components as dmc
import dash_bootstrap_components as dbc
from dash_iconify import DashIconify
from data_preparation import *
from graph_without_callback import *
from components import *


app_name = "tracker"

dash.register_page(
    __name__, path=f"/{app_name}", title=app_name, description=app_name, name=app_name)

layout = html.Div(id=app_name, className="container container-lg layout", children=[

    html.H1("Data Analysis", className="display-4"),

    html.Div(className="preambule", children=[
        dcc.Markdown(
            "Bienvenue dans notre tableau de bord dédié à l'analyse des données relatives au terrorisme dans le monde. Ce tableau de bord a pour objectif de vous fournir une vue approfondie et dynamique de l'évolution des actes terroristes à travers le temps et l'espace. À travers une série de visualisations interactives et de données actualisées, nous explorerons les tendances, les régions les plus touchées, les groupes terroristes les plus actifs, et bien plus encore. Comprendre le terrorisme nécessite une définition claire et une analyse précise, et c'est précisément ce que nous nous efforçons de vous offrir ici. Préparez-vous à plonger dans l'univers complexe et évolutif du terrorisme, en utilisant les données pour mieux comprendre ce phénomène mondial.",

            className="preambule_text",
        )
    ]),
    
    
    html.H1("Analyse (Géospatiale) Des Tendances De L'activité Terroriste Dans Le Monde", className="display-4"),


    html.Div(className="row align-items-center", children=[
        html.Div(className="col-lg-9 carte", children=[
            dcc.Loading(dcc.Graph(id="geo-map"),
                        color="firebrick", type="dot"),
        ]),

        html.Div(className="col-lg-3", children=[
            html.H4("Europe de L'Ouest", className=""),
            dcc.Markdown(
                "Dans l'ensemble, le nombre d'attaques terroristes dans le monde a augmenté de manière significative au fildes décennies. Cette augmentation peut être attribuée à plusieurs facteurs, notamment la montée de groupesterroristes, la facilité accrue de communication et de recrutement grâce à Internet, ainsi des cellules terroristes dans de nombreux pays.",

                className="preambule_text",
            ),
        ])
    ]),



    html.Div(className="row align-items-center mt-5", children=[

        html.Div(className="col-lg-6 carte", children=[
            dcc.Loading(dcc.Graph(id="serie-area",
                        config=dict(displayModeBar=False)))
        ]),

        html.Div(className="col-lg-6 carte", children=[
            dcc.Loading(dcc.Graph(id="timeseries-by-category",
                        config=dict(displayModeBar=False)),),

            html.Div(className="selection d-flex justify-content-center mt-2", children=[
                dmc.ChipGroup(value="attacktype", id="category-select", children=[
                    dmc.Chip(x, value=y, size="sm", color="red")
                    for x, y in zip(
                        ["Par mode d'attaque", "Par cibles visées",
                            "Par armes utilisées"],
                        ["attacktype", "targtype", "weaptype1"]
                    )
                ]),
            ]),

            html.Div(className="selection d-flex justify-content-center mt-2", children=[
                choice_serie_type('choice_serie_type_crt'),
            ]),
        ])

    ]),


    html.Div(className="row align-items-center mt-5", id="share"),


    html.Div(className="row align-items-center mt-5", children=[

        html.Div(className="col-lg-12 carte", children=[
            dcc.Loading(dcc.Graph(id="global-rate", config=dict(displayModeBar=False)))
        ]),
    ]),


    html.Div(className="row mt-5", children=[

        html.Div(className="title-section mb-3", children=[
            html.Div(className="dash"),
            html.H2("Étude De La gravité De L'attaque", className="")
        ]),

        dcc.Markdown(
            """
            Le "niveau de violence" dans fait référence à la gravité ou à l'ampleur des actes terroristes commis. Il peut être mesuré de différentes manières, notamment en tenant compte des éléments suivants :

            **Nombre de Victimes** : Le nombre de personnes tuées, blessées ou prises en otage lors d'un acte terroriste est l'une des mesures les plus directes du niveau de violence. Plus le nombre de victimes est élevé, plus l'acte est considéré comme violent.
            
            **Dommages Matériels** : L'étendue des dommages matériels causés par un acte terroriste peut également être un indicateur du niveau de violence. Cela peut inclure des dégâts aux biens, aux infrastructures ou à l'environnement. (Voir Figure 19)
            
            **Type d'Armes Utilisées** : Les types d'armes ou d'explosifs utilisés dans l'attaque peuvent influencer le niveau de violence. Par exemple, une explosion causée par un engin explosif de grande puissance est généralement plus violente qu'une attaque au couteau. (Voir Figure 1)
            
            **Ciblage** : Les cibles des attaques peuvent également refléter le niveau de violence. Les attaques visant des civils non armés sont souvent considérées comme particulièrement violentes, tandis que celles visant des forces de l'ordre ou des cibles militaires peuvent être perçues différemment. (Voir Figure 1)
            
            Nous nous contenterons d'analyser la gravité de l'attaque en fonction de leur impact sur les personnes, c'est-à-dire en prenant en compte le nombre de victimes (personnes décédées et blessées) repartir par classe.
            """,

            className="preambule_text",
        ),

    ]),


    html.Div(className="row justify-content-center", children=[

        html.Div(className="col-lg-4", children=[
            html.Span("Selectionner une métrique", className="text-white"),
            dcc.Dropdown(
                id="severity-metric",
                options=[
                    {"label": x, "value": y}
                    for x, y in zip(["Décès", "Victimes (Blessés + Décès)"], ["nkill", "casualties"])
                ],

                value="nkill",
                placeholder="Selection",
            )
        ]),

    ]),


    html.Div(className="row align-items-center mt-3", children=[

        html.Div(className="col-lg-5 carte", children=[

            html.Div(className="mb-2", children=[
                dcc.Loading(dcc.Graph(config=dict(
                    displayModeBar=False), id="pie-severity"),)
            ])

        ]),

        html.Div(className="col-lg-7 carte", children=[

            dcc.Loading(dcc.Graph(config=dict(
                displayModeBar=False), id="attack-by-severity"),),

            html.Div(className="selection d-flex justify-content-center mt-2", children=[
                dmc.ChipGroup(value="relative", id="rel-abs", children=[
                    dmc.Chip(x, value=y, size="sm", color="red")
                    for x, y in zip(
                        ["Série relative", "Série absolue"],
                        ["relative", "absolue"]
                    )
                ]),
            ])
        ]),

    ]),


    html.Div(className="row mt-3", children=[

        dcc.Markdown(
            "Dans l'ensemble, le nombre d'attaques terroristes dans le monde a augmenté de manière significative au fildes décennies. Cette augmentation peut être attribuée à plusieurs facteurs, notamment la montée de groupesterroristes, la facilité accrue de communication et de recrutement grâce à Internet, ainsi que les conflitsrégionaux et internationaux. Au cours de cette période, des groupes terroristes tels qu'Al-Qaïda et l'Étatislamique (ISIS) sont devenus des acteurs mondiaux majeurs du terrorisme, lançant des attaques à l'échelleinternationale et inspirant des cellules terroristes dans de nombreux pays.",

            className="preambule_text",
        ),

    ])


])
