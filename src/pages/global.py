import dash
from dash import html, dcc
import dash_mantine_components as dmc
import dash_bootstrap_components as dbc
from dash_iconify import DashIconify
from apps import header, thesis
from data_preparation import *
from graph_without_callback import *
from components import *


app_name = "overview"

dash.register_page(__name__, path=f"/", title=app_name, description=app_name, name=app_name)

active_tab_style = {
    "font-family": "serif",
    "border-bottom": "none"
}

tab_style={"marginLeft": "auto"}


layout = html.Div(id=app_name, className="container-fluid container-lg layout", children=[
    
    thesis.thesis,
    
    header.navigation,
    
    dmc.Affix(position={"bottom": 20, "left": 15}, className="affix", children=[
        # dmc.Button("I'm in an Affix Component", className="btn-danger"),
        html.Div(className="affix-graph", children=[
            dcc.Loading(dcc.Graph(id="geo-map_"), color="red", type="dot"),
        ])
    ]),
    
    
    
    
    html.Div(className="row align-items-center my-5 py-5", children=[
                
        html.Div(className="col-lg-7", children=[
            dcc.Markdown(
                """
                # Apercu Général Des Tendances De
                # L'activités Terroriste
                # Dans Le Monde  
                # 1970 - 2020
                Une analyse statistique globale
                """
            ),
        ]),

        
        html.Div(className="col-lg-5", children=[
            
            html.Div(className="row justify-content-center", children=[
                
                html.Div(className="col", children=[
                    
                    html.Div(className="row justify-content-center", children=[
                        
                        html.Div(className="col-lg-4", children=[
                            html.Span("Zone géographique", className=""),
                            dcc.Dropdown(
                                id="dropdown-geo",
                                options=[{"label":"Monde", "value":"Monde"}]+
                                
                                        [{"label":"Par continent------------------------------", "disabled": True, "value":"Monde"}]+
                                        
                                        [{"label": html.Span([x], style={'color': 'rgb(252,187,161)'}), "value": x,} 
                                         for x in sorted(list(df.continent.unique()))]+
                                        
                                        [{"label":"Par region---------------------------------", "disabled": True, "value":"Monde"}]+
                                        
                                        [{"label": html.Span([y], style={'color': 'rgb(254,224,210'}),"value": y}
                                         for y in sorted(list(df.region.unique()))]+
                                        
                                        [{"label":"Par pays---------------------------------", "disabled": True, "value":"Monde"}]+
                                        
                                        [{"label": html.Span([z], style={'color': 'rgb(255,245,240)'}),"value": z}
                                         for z in sorted(list(df.flag_country.unique()))]
                                ,
                                value="Monde",
                                placeholder="Selection",
                                searchable=True,
                                clearable=True,
                                style={"color": "white"}
                            )
                        ]),
                        
                        html.Div(className="col-lg-4", children=[
                            html.Span("Cause", className=""),
                            dcc.Dropdown(
                                id="dropdown-cause",
                                options=[
                                    {"label": x, "value": y} 
                                    for x, y in zip(["Incidences", "Blessés", "Décès"], ["size", "nwound", "nkill"])
                                ],
                                value="size",
                                placeholder="Selection",
                            )
                        ]),
                        
                        html.Div(className="col-lg-4", children=[
                            html.Span("Groupe terroriste", className="d-block"),
                            dcc.Dropdown(
                                id="dropdown-group",
                                options=[
                                    {"label": x, "value": x} for x in ["All group"] + sorted(terrorist_group) 
                                ],
                                value="All group",
                                placeholder="Selection",
                            ),
                        ]),
                        
                        
                        html.Div(className="col-lg-4", children=[
                            html.Span("Type d'attaque", className="d-block"),
                            dcc.Dropdown(
                                id="dropdown-attack",
                                options=[
                                    {"label": x, "value": x} for x in ["All attack type"] + sorted(terrorist_attack)
                                ],
                                value="All attack type",
                            ),
                        ]),
                        
                        html.Div(className="col-lg-4", children=[
                            html.Span("Cible visées", className="d-block"),
                            dcc.Dropdown(
                                id="dropdown-target",
                                options=[
                                    {"label": x, "value": x} for x in ["All target"] + sorted(terrorist_targtype)
                                ],
                                value="All target",
                            ),
                        ]),
                        
                        html.Div(className="col-lg-4", children=[
                            html.Span("Armes utilisées", className="d-block"),
                            dcc.Dropdown(
                                id="dropdown-weapon",
                                options=[
                                    {"label": x, "value": x} for x in ["All weapons"] + sorted(terrorist_weaptype)
                                ],
                                value="All weapons",
                            )
                        ]),
                        
                        html.Div(className="mt-3 col-lg-8", children=[
                            html.Div(className="text-enter", children=[
                                html.P("Selectionner une plage d'année", className="mb-3"),
                            ]),
                            
                            dmc.RangeSlider(
                                id="date-range-slider",
                                min=list(df.year.unique())[0], 
                                max=list(df.year.unique())[-1], 
                                value=[1970, 2020],
                                step=1, size=1.5, color="red",
                                marks=[
                                    {"value": 1970, "label": "1970"},
                                    {"value": 2020, "label": "2020"},
                                ],
                                labelAlwaysOn=True,
                                labelTransition="fade",
                                style={
                                    "font-family": "serif",
                                    "color": "white !importtant",
                                }
                            ),

                        ]),
                        
                    ]),
                    
                    
                ])
                
            ]),
            
            
            html.Div(className="text-center mt-5", children=[
        
                dbc.Button(n_clicks=0, className="btn", id="reset", children=[
                    DashIconify(icon="system-uicons:reset", width=20), " Réinitialiser"
                ]) 
                  
            ]),
                
        ])
    ]),

    
    html.Div(className="row align-items-center mt-5", children=[
        
        html.Div(className="col-lg-6", children=[
            dcc.Loading(dcc.Graph(id="global-incidence-timeseries", config=dict(displayModeBar=False)))
        ]),
        
        html.Div(className="col-lg-6", children=[
            dcc.Loading(dcc.Graph(id="by-continent", config=dict(displayModeBar=False))),
            choice_serie_type('choice_serie_type_continent')
        ])
        
    ]),
    
    html.Div(className="row mt-3", children=[
        
        dcc.Markdown(
            "Dans l'ensemble, le nombre d'attaques terroristes dans le monde a augmenté de manière significative au fildes décennies. Cette augmentation peut être attribuée à plusieurs facteurs, notamment la montée de groupesterroristes, la facilité accrue de communication et de recrutement grâce à Internet, ainsi que les conflitsrégionaux et internationaux. Au cours de cette période, des groupes terroristes tels qu'Al-Qaïda et l'Étatislamique (ISIS) sont devenus des acteurs mondiaux majeurs du terrorisme, lançant des attaques à l'échelleinternationale et inspirant des cellules terroristes dans de nombreux pays.",
                                    
            className="preambule_text",
        ),
        
    ]),
    
    html.Div(className="row align-items-center mt-5", children=[
        
        html.Div(className="col-lg-6", children=[
            dcc.Loading(dcc.Graph(id="by-region", config=dict(displayModeBar=False))),
            choice_serie_type('choice_serie_type_region')
        ]),
        
        html.Div(className="col-lg-6", children=[
            dcc.Loading(dcc.Graph(id="country-timeseries", config=dict(displayModeBar=False))),
            choice_serie_type('choice_serie_type_countries')
        ])
        
    ]),
    
    html.Div(className="row mt-3", children=[
        
        dcc.Markdown(
            "Dans l'ensemble, le nombre d'attaques terroristes dans le monde a augmenté de manière significative au fildes décennies. Cette augmentation peut être attribuée à plusieurs facteurs, notamment la montée de groupesterroristes, la facilité accrue de communication et de recrutement grâce à Internet, ainsi que les conflitsrégionaux et internationaux. Au cours de cette période, des groupes terroristes tels qu'Al-Qaïda et l'Étatislamique (ISIS) sont devenus des acteurs mondiaux majeurs du terrorisme, lançant des attaques à l'échelleinternationale et inspirant des cellules terroristes dans de nombreux pays.",
                                    
            className="preambule_text",
        ),
        
    ]),
    
        
    
    html.Div(className="row align-items-center mt-5 pt-5", children=[
                
        html.Div(className="title-section mb-3", children=[
            html.Div(className="dash"),
            html.H2("Une Meilleure Vue D'ensemble", className="")
        ]),
        
        html.Div(className="col-lg-8", children=[
            dcc.Graph(config=dict(displayModeBar=False), figure=quincenal_average())
        ]),
        
        html.Div(className="col-lg-4", children=[
            dcc.Markdown(
                """
                Nous utilison une moyenne quinquennale (sur une période de 5 ans) pour analyser les tendances à long terme dans les données temporelles des acivités terroristes, en réduisant le bruit et en fournissant une vue d'ensemble plus claire des évolutions sur plusieurs années.
                
                On constate que les activités terroristes et leurs conséquences connaissent un fort accroissement à partir des années 2005 à 2017. Cette augmentation peut être attribuée à plusieurs facteurs, notamment la montée de groupes terroristes, la facilité accrue de communication et de recrutement grâce à Internet, ainsi que les conflits régionaux et internationaux
                
                Precisement, entre 1998 et 2014 il y a eu un taux d'accroissent de 120% soit une multiplication par 3 du nombres d'attacque terroriste, suivie egalement d'un nombre de décès élevé
                """,
                                        
                className="preambule_text",
            )
        ]),
        
    ]),
    
    html.Div(className="row align-items-center mt-5", children=[
        
        html.Div(className="col-lg-5", children=[
            dcc.Markdown(
                """
                On constate que les activités terroristes et leurs conséquences connaissent un fort accroissement à partir des années 2005 à 2017. Cette augmentation peut être attribuée à plusieurs facteurs, notamment la montée de groupes terroristes, la facilité accrue de communication et de recrutement grâce à Internet, ainsi que les conflits régionaux et internationaux
                
                Precisement, entre 1998 et 2014 il y a eu un taux d'accroissent de 120% soit une multiplication par 3 du nombres d'attacque terroriste, suivie egalement d'un nombre de décès élevé
                """
            ),
            html.Div(className="mt-1", children=[
                dcc.Graph(config=dict(displayModeBar=False), id="world-top-affected-rest-of-world")
            ]),
            
            dcc.Markdown(
                """
                Precisement, entre 1998 et 2014 il y a eu un taux d'accroissent de 120% soit une multiplication par 3 du nombres d'attacque terroriste, suivie egalement d'un nombre de décès élevé
                """
            ),
            
            html.Div(className="mt-1", children=[
                dcc.Graph(config=dict(displayModeBar=False), id="world-top-affected-rest-of-world2")
            ]),
        ]),
        
        html.Div(className="col-lg-7", children=[
            dcc.Graph(config=dict(displayModeBar=False), id="top-country-and-world")
        ]),
        
    ]),
    
    html.Div(className="row my-5 py-5", children=[]),
    
    
    
    
    html.Div(className="row my-5 align-items-center", children=[
        html.Div(className="col-lg-7", children=[
            dcc.Markdown(
                """
                # Analyse (Géospatiale) 
                # Des Tendances De
                # L'activité Terroriste
                # Dans Le Monde
                # 1970 et 2020
                Une analyse statistique détaillée
                """,
                className="fw-bold"
            )
        ]),
        
    
        
        html.Div(className="col-lg-5", children=[
            html.Div(className="row justify-content-center", children=[
                        
                html.Div(className="col-lg-4", children=[
                    html.Span("Zone géographique", className=""),
                    dcc.Dropdown(
                        id="filter-geo",
                        options=[{"label":"Monde", "value":"Monde"}]+
                        
                                [{"label":"Continental", "disabled": True, "value":"Monde"}]+
                                
                                [{"label": html.Span([x], style={'color': 'rgb(252,187,161)'}), "value": x,} 
                                 for x in sorted(list(df.continent.unique()))]+
                                
                                [{"label":"Regional", "disabled": True, "value":"Monde"}]+
                                
                                [{"label": html.Span([y], style={'color': 'rgb(254,224,210'}),"value": y}
                                 for y in sorted(list(df.region.unique()))]+
                                
                                [{"label":"Pays les pays touches", "disabled": True, "value":"Monde"}]+
                                
                                [{"label": html.Span([z], style={'color': 'rgb(255,245,240)'}),"value": z}
                                 for z in sorted(countries_most_affected)]
                        ,
                        value="Monde",
                        placeholder="Selection",
                        searchable=True,
                        clearable=True,
                        style={"color": "white"}
                    )
                ]),
                
                html.Div(className="col-lg-4", children=[
                    html.Span("Métrique", className=""),
                    dcc.Dropdown(
                        id="cause",
                        options=[
                            {"label": x, "value": y} 
                            for x, y in zip(["Incidences", "Blessés", "Décès", "Victimes (Blessés + Décès)"], ["size", "nwound", "nkill", "casualties"])
                        ],
                        value="size",
                        placeholder="Selection",
                    )
                ]),
                
                html.Div(className="col-lg-4", children=[
                    html.Span("Groupe terroriste", className="d-block"),
                    dcc.Dropdown(
                        id="group",
                        options=[
                            {"label": x, "value": x} for x in ["All group"] + sorted(terrorist_group) 
                        ],
                        value="All group",
                        placeholder="Selection",
                    ),
                ]),
                        
                        
                html.Div(className="col-lg-4", children=[
                    html.Span("Type d'attaque", className="d-block"),
                    dcc.Dropdown(
                        id="attack",
                        options=[
                            {"label": x, "value": x} for x in ["All attack type"] + sorted(terrorist_attack)
                        ],
                        value="All attack type",
                    ),
                ]),
                
                html.Div(className="col-lg-4", children=[
                    html.Span("Cible visées", className="d-block"),
                    dcc.Dropdown(
                        id="target",
                        options=[
                            {"label": x, "value": x} for x in ["All target"] + sorted(terrorist_targtype)
                        ],
                        value="All target",
                    ),
                ]),
                        
                html.Div(className="col-lg-4", children=[
                    html.Span("Armes utilisées", className="d-block"),
                    dcc.Dropdown(
                        id="weapon",
                        options=[
                            {"label": x, "value": x} for x in ["All weapons"] + sorted(terrorist_weaptype)
                        ],
                        value="All weapons",
                    )
                ]),
                        
                html.Div(className="mt-3 col-lg-8", children=[
                    html.Div(className="text-enter", children=[
                        html.P("Selectionner une plage d'année", className="mb-3"),
                    ]),
                    
                    dmc.RangeSlider(
                        id="range-slider",
                        min=list(df.year.unique())[0], 
                        max=list(df.year.unique())[-1], 
                        value=[1970, 2020],
                        step=1, size=1.5, color="red",
                        marks=[
                            {"value": 1970, "label": "1970"},
                            {"value": 2020, "label": "2020"},
                        ],
                        labelAlwaysOn=True,
                        labelTransition="fade",
                        style={
                            "font-family": "serif",
                            "color": "white !importtant",
                        }
                    ),
                ]), 
            ]),
            
            html.Div(className="row justify-content-center text-center mt-5", children=[
                
                html.Div(className="col-lg-4", children=[
        
                    dbc.Button(n_clicks=0, className="btn", id="reset-data", children=[
                        DashIconify(icon="system-uicons:reset", width=20), " Réinitialiser"
                    ]) 
                    
                ]),
        
            ]),
        ])
    ]),
    
    

    html.Div(className="row align-items-center", children=[
        html.Div(className="col-lg-9", children=[
            dcc.Loading(dcc.Graph(id="geo-map"), color="firebrick", type="dot"),
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
        
        html.Div(className="col-lg-6", children=[
            dcc.Loading(dcc.Graph(id="serie-area", config=dict(displayModeBar=False)))
        ]),
        
        html.Div(className="col-lg-6", children=[
            dcc.Loading(dcc.Graph(id="timeseries-by-category", config=dict(displayModeBar=False)),),
            
            html.Div(className="selection d-flex justify-content-center mt-2", children=[
                dmc.ChipGroup(value="attacktype", id="category-select", children=[
                    dmc.Chip(x, value=y, size="sm", color="red") 
                    for x, y in zip(
                        ["Par mode d'attaque", "Par cibles visées", "Par armes utilisées"], 
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
        
        html.Div(className="col-lg-12", children=[
            dcc.Loading(dcc.Graph(id="global-rate", config=dict(displayModeBar=False)))
        ]),
    ]),
    
    
    html.Div("space", className="separate my-5"),
    
    
    html.Div(className="row", children=[
                
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
        
        html.Div(className="col-lg-5", children=[
            
            html.Div(className="mb-2", children=[
                dcc.Loading(dcc.Graph(config=dict(displayModeBar=False), id="pie-severity"),)
            ])
            
        ]),
        
        html.Div(className="col-lg-7", children=[
            
            dcc.Loading(dcc.Graph(config=dict(displayModeBar=False), id="attack-by-severity"),),
            
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
        
    ]),
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    html.Div("space", className="separate my-5"),
    
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
            dcc.Loading(dcc.Graph(id="period-timeseries", config=dict(displayModeBar=False)),)
        ]),
        
        html.Div(className="col-lg-5", children=[
            dcc.Loading(dcc.Graph(id="period-distribution", config=dict(displayModeBar=False)))
        ])
        
    ]),
    
    
    html.Div(className="row justify-content-center align-items-center mt-5 ", children=[
        
        html.Div(className="col-lg-8", children=[            
            
            dcc.Loading(dcc.Graph(config=dict(displayModeBar=False), id="mean-day"), color="red")
        ]),
        
        html.Div(className="col-lg-4", children=[
            html.Div(className="mb-2", children=[
                html.P("Année"),
                dcc.Slider(1970, 2020, 1, value=2020, marks=None, included=False, id="slider",
                    tooltip={"placement": "bottom", "always_visible": True}
                ),
            ]),
            dcc.Markdown(
                "Bienvenue dans notre tableau de bord dédié à l'analyse des données relatives au terrorisme dans le monde. Ce tableau de bord a pour objectif de vous fournir une vue approfondie et dynamique de l'évolution des actes terroristes à travers le temps et l'espace. À travers une série de visualisations interactives et de données actualisées, nous explorerons les tendances, les régions les plus touchées, les groupes terroristes les plus actifs, et bien plus encore. Comprendre le terrorisme."
            ),
        ]),
        
    ]),
    
    
    
    html.Div(className="row align-items-center mt-5", children=[
        
        html.Div(className="col-lg-4", children=[
            dcc.Loading(dcc.Graph(id="month-timeseries", config=dict(displayModeBar=False)),)
        ]),
        
        html.Div(className="col-lg-8", children=[
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
                            dcc.Loading(dcc.Graph(id="serie-relative-absolue", config=dict(displayModeBar=False))),
                            
                            html.Div(className="selection d-flex justify-content-center mt-2", children=[
                                dmc.ChipGroup(value="attacktype", id="slct-category", children=[
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
            ])
        ])
        
    ]),
    
    html.Div(className="row mt-3", children=[
        
        dcc.Markdown(
            "Dans l'ensemble, le nombre d'attaques terroristes dans le monde a augmenté de manière significative au fildes décennies. Cette augmentation peut être attribuée à plusieurs facteurs, notamment la montée de groupesterroristes, la facilité accrue de communication et de recrutement grâce à Internet, ainsi que les conflitsrégionaux et internationaux. Au cours de cette période, des groupes terroristes tels qu'Al-Qaïda et l'Étatislamique (ISIS) sont devenus des acteurs mondiaux majeurs du terrorisme, lançant des attaques à l'échelleinternationale et inspirant des cellules terroristes dans de nombreux pays.",
                                    
            className="preambule_text",
        ),
        
    ]),
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    html.Div("space", className="separate my-5"),

    
    html.Div(className="row align-items-center", children=[
                
        html.Div(className="title-section mb-3", children=[
            html.Div(className="dash"),
            html.H2("Repartition: Tendances De Plus Haut Niveau", className="")
        ]),
        
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
                html.Div(className="col-12 col-md-6 col-lg-6", children=[
                    dcc.Loading(dcc.Graph(id="pie-group", config=dict(displayModeBar=False)), type="circle")
                ]),
                
                html.Div(className="col-12 col-md-6 col-lg-6", children=[
                    dcc.Loading(dcc.Graph(id="pie-weapon", config=dict(displayModeBar=False)), type="circle")
                ]),
                
                html.Div(className="col-12 col-md-6 col-lg-6", children=[
                    dcc.Loading(dcc.Graph(id="pie-attack", config=dict(displayModeBar=False)), type="circle")
                ]),
                
                html.Div(className="col-12 col-md-6 col-lg-6", children=[
                    dcc.Loading(dcc.Graph(id="pie-target", config=dict(displayModeBar=False)), type="circle")
                ])
            ]),
        ]),
        
        html.Div(className="col-12", children=[
            dcc.Markdown(
                "Bienvenue dans notre tableau de bord dédié à l'analyse des données relatives au terrorisme dans le monde. Ce tableau de bord a pour objectif de vous fournir une vue approfondie et dynamique de l'évolution des actes terroristes à travers le temps et l'espace. À travers une série de visualisations interactives et de données actualisées, nous explorerons les tendances, les régions les plus touchées, les groupes terroristes les plus actifs, et bien plus encore. Comprendre le terrorisme."
            ),
        ]),
        
    ]),
    
    
    html.Div("space", className="separate my-5"),
    
    
    html.Div(className="row align-items-center", children=[
                
        html.Div(className="title-section mb-3", children=[
            html.Div(className="dash"),
            html.H2("Les Grands Groupes Terroristes", className="")
        ]),
        
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
        
        html.Div(className="col-lg-8", children=[
            dcc.Graph(config=dict(displayModeBar=False), id="sankey-graph")
        ]),
        
    ]),
    
    
    html.Div("space", className="separate my-5"),
    
    
    
    html.Div(className="row align-items-center justify-content-center", children=[
                
        html.Div(className="title-section mb-3", children=[
            html.Div(className="dash"),
            html.H2("Analyse Comparative de Divers Aspects du Terrorisme", className="")
        ]),
        
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
                    ["Diagramme circulaire (repartition en %)", "Evolution (relative) dans le temps"], 
                    ["pie", "bar"]
                )
            ])
        ])
        
    ]),
    
    
    html.Div(className="row justify-content-center align-items-center mt-3", children=[
                
        html.Div(className="col-lg-6", children=[
            dcc.Graph(id="pie-success", config=dict(displayModeBar=False))
        ]),
        
        html.Div(className="col-lg-6", children=[
            dcc.Graph(id="pie-suicide", config=dict(displayModeBar=False))
        ]),
        
        html.Div(className="col-lg-6", children=[
            dcc.Graph(id="pie-individual", config=dict(displayModeBar=False))
        ]),
        
        html.Div(className="col-lg-6", children=[
            dcc.Graph(id="pie-crit", config=dict(displayModeBar=False))
        ]),
        
        html.Div(className="mt-3", children=[
            dcc.Markdown(
                "Bienvenue dans notre tableau de bord dédié à l'analyse des données relatives au terrorisme dans le monde. Ce tableau de bord a pour objectif de vous fournir une vue approfondie et dynamique de l'évolution des actes terroristes à travers le temps et l'espace. À travers une série de visualisations interactives et de données actualisées, nous explorerons les tendances, les régions les plus touchées, les groupes terroristes les plus actifs, et bien plus encore. Comprendre le terrorisme."
            ),
        ]),
        
    ]),
    
    
    html.Div("space", className="separate my-5"),
    
    
    html.Div(className="title-section mb-3", children=[
        html.Div(className="dash"),
        html.H2("Impact Économiques Des activités Terroriste", className="")
    ]),
     
     html.Div(className="row mb-3", children=[
        
        dcc.Markdown(
            "Dans l'ensemble, le nombre d'attaques terroristes dans le monde a augmenté de manière significative au fildes décennies. Cette augmentation peut être attribuée à plusieurs facteurs, notamment la montée de groupesterroristes, la facilité accrue de communication et de recrutement grâce à Internet, ainsi que les conflitsrégionaux et internationaux. Au cours de cette période, des groupes terroristes tels qu'Al-Qaïda et l'Étatislamique (ISIS) sont devenus des acteurs mondiaux majeurs du terrorisme, lançant des attaques à l'échelleinternationale et inspirant des cellules terroristes dans de nombreux pays.",
                                    
            className="preambule_text",
        ),
        
    ]),
     
     html.Div(className="row align-items-center mt-5", children=[
         
         html.Div(className="col-lg-6", children=[
            dcc.Loading(dcc.Graph(id="series-damages", config=dict(displayModeBar=False)),),
            html.Div(className="selection d-flex justify-content-center mt-2", children=[
                dmc.ChipGroup(value="1", id="select-property", children=[
                    dmc.Chip(x, value=y, size="sm", color="red") 
                    for x, y in zip(
                        ["Ayant causé des dégâts matériels", "Sans dégâts matériels"], 
                        ["1", "0"]
                    )
                ]),
            ])
        ]),
        
        html.Div(className="col-lg-6", children=[
            dcc.Loading(dcc.Graph(id="graph", config=dict(displayModeBar=False)),),
            html.Div(className="selection d-flex justify-content-center mt-2", children=[
                dmc.ChipGroup(value="absolue", id="rel-abs-damage", children=[
                    dmc.Chip(x, value=y, size="sm", color="red") 
                    for x, y in zip(
                        ["Série temporelle relative", "Série temporelle absolue"], 
                        ["relative", "absolue"]
                    )
                ])
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
         
         html.Div(className="col-lg-6", children=[
            dcc.Loading(dcc.Graph(id="repartition-damages", config=dict(displayModeBar=False)))
        ]),
        
        html.Div(className="col-lg-6", children=[
            dcc.Loading(dcc.Graph(config=dict(displayModeBar=False), id="repartition-dollars"))
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
        
        html.Div(className="col-lg-8", children=[
            dcc.Graph(id="number-attack-with-damage-by-category", config=dict(displayModeBar=False))
        ]),
        
    ]),
     
     
    html.Div(className="row justify-content-center align-items-center mt-5", children=[
        
        html.Div(className="col-lg-12", children=[
            html.H4("Carte graphique: repatition des attaque par coût (en dollars $)"),
            dcc.Markdown(
                "Bienvenue dans notre tableau de bord dédié à l'analyse des données relatives au terrorisme dans le monde. Ce tableau de bord a pour objectif de vous fournir une vue approfondie et dynamique de l'évolution des actes terroristes à travers le temps et l'espace. À travers une série de visualisations interactives et de données actualisées, nous explorerons les tendances, les régions les plus touchées, les groupes terroristes les plus actifs, et bien plus encore. Comprendre le terrorisme."
            ),
        ]),
        
    ]),
     
     
     
    html.Div(className="row justify-content-center align-items-center mt-5 pt-5", children=[
        
        html.Div(className="col-lg-8", children=[
            dcc.Graph(config=dict(displayModeBar=False), figure=property_graph())
        ]),
        
        html.Div(className="col-lg-4", children=[
            dcc.Markdown(
                "Bienvenue dans notre tableau de bord dédié à l'analyse des données relatives au terrorisme dans le monde. Ce tableau de bord a pour objectif de vous fournir une vue approfondie et dynamique de l'évolution des actes terroristes à travers le temps et l'espace. À travers une série de visualisations interactives et de données actualisées, nous explorerons les tendances, les régions les plus touchées, les groupes terroristes les plus actifs, et bien plus encore. Comprendre le terrorisme."
            ),
        ]),
        
    ]),
     
     
     html.Div("space", className="separate my-5"),
     
     
     
    html.Div(className="row my-5 align-items-center", children=[
        html.Div(className="col-lg-7", children=[
            dcc.Markdown(
                """
                # 2014: Une Année de 
                # Forte Croissance de 
                # l'Activité Terroriste
                """,
                className="fw-bold"
            )
        ])
    ])
    
    
])


