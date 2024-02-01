import dash
import dash_deck as ddk
import dash_mantine_components as dmc

from dash import html, dcc

from data_preparation import *
from graph_without_callback import *
from components import *
from callback.general import *


app_name = "Generalite"

dash.register_page(__name__, path=f"/", title=app_name, description=app_name, name=app_name)

dropdown_items = [
	dac.BoxDropdownItem(url="https://www.google.com", children="Link to google"),
	dac.BoxDropdownItem(url="#", children="item 2"),
	dac.BoxDropdownDivider(),
	dac.BoxDropdownItem(url="#", children="item 3")
]


layout = html.Div(id=app_name, className="container container-lg layout", children=[
    
    html.H1("Généralité", className="display-3 mt-2"),
    
    html.Div(className="preambule", children=[
        dcc.Markdown(
            "Bienvenue dans notre tableau de bord dédié à l'analyse des données relatives au terrorisme dans le monde. Ce tableau de bord a pour objectif de vous fournir une vue approfondie et dynamique de l'évolution des actes terroristes à travers le temps et l'espace. À travers une série de visualisations interactives et de données actualisées, nous explorerons les tendances, les régions les plus touchées, les groupes terroristes les plus actifs, et bien plus encore. Comprendre le terrorisme nécessite une définition claire et une analyse précise, et c'est précisément ce que nous nous efforçons de vous offrir ici. Préparez-vous à plonger dans l'univers complexe et évolutif du terrorisme, en utilisant les données pour mieux comprendre ce phénomène mondial.",
                                    
            className="preambule_text",
        ),
        
    ]),
    
    
    html.Div(className="d-flex align-items-center justify-content-between mt-5", children=[
        
        html.Div(className="d-flex align-items-center justify-content-center carte mx-2", children=[
            html.Div(className="", children=[
                html.Img(
                    src=dash.get_asset_url('atr.png'),
                    className="div-img img-responsive rounded-circle me-2",
                    style={
                        "height": "70px",
                        "width": "70px",
                    }
                ),
            ]),

            html.Div(className="", children=[
                html.H1(f"{len(raw_data)}", className="text-success"),
                html.Small("plus encore. Comprendre le terrorisme nécessite une définition claire et une analyse précise, et c'est précisément ce que nous", className=""),
            ]),
        ]),
        
        
        html.Div(className="d-flex align-items-center justify-content-center carte mx-2", children=[
            html.Div(className="", children=[
                html.Img(
                    src=dash.get_asset_url('death.jpg'),
                    className="div-img img-responsive rounded-circle me-2",
                    style={
                        "height": "70px",
                        "width": "70px",
                    }
                ),
            ]),

            html.Div(className="", children=[
                html.H1(f"{int(raw_data['nkill'].sum())}", className="text-danger"),
                html.Small("plus encore. Comprendre le terrorisme nécessite une définition claire et une analyse précise, et c'est précisément ce que nous", className=""),
            ]),
        ]),
        
        html.Div(className="d-flex align-items-center justify-content-center carte mx-2", children=[
            html.Div(className="", children=[
                html.Img(
                    src=dash.get_asset_url('injured.png'),
                    className="div-img img-responsive rounded-circle me-2",
                    style={
                        "height": "70px",
                        "width": "70px",
                    }
                ),
            ]),

            html.Div(className="", children=[
                html.H1(f"{int(raw_data['nwound'].sum())}", className="text-warning"),
                html.Small(
                    "plus encore. Comprendre le terrorisme nécessite une définition claire et une analyse précise, et c'est précisément ce que nous", className=""),
            ]),
        ]),
        
    ]),
    
    
    html.Div(className="row gx-5 align-items-center mt-5", children=[

        html.Div(className="col-12 carte", children=[
            html.Div(id="daily"),
        ])

    ]),
    
    
    html.Div(className="row align-items-center mt-5", children=[

        dac.TabItem(id='content_cards', active=False, children=[
                dac.Box(
                    [
                        dac.BoxHeader(
                            dac.BoxDropdown(dropdown_items),
                            collapsible=True,
                            closable=True,
                            title="Daily distribution"
                        ),
                        dac.BoxBody(
                            dcc.Graph(
                                id="dist-fig",
                                config=dict(displayModeBar=False),
                            )
                        )
                    ],
                    #color='info',
                    width=12,
                    elevation=1,
                    solid_header=True
                ),
            ])     

    ]),
    
    
    
    html.Div(className="row align-items-center mt-5", children=[

        html.Div(className="col-lg-12 carte", children=[
            html.Div(id="echart"),
        ]),
        
        html.Div(className="mt-3 col-12", children=[
            dcc.Markdown(
                "Bienvenue dans notre tableau de bord dédié à l'analyse des données relatives au terrorisme dans le monde. Ce tableau de bord a pour objectif de vous fournir une vue approfondie et dynamique de l'évolution des actes terroristes à travers le temps et l'espace. À travers une série de visualisations interactives et de données actualisées, nous explorerons ce phénomène mondial.",

                className="preambule_text",
            ),

        ]),

    ]),
    
    html.Div(className="row align-items-center mt-5", children=[

        html.Div(className="col-lg-8 carte", children=[
            dcc.Graph(config=dict(displayModeBar=False),
                      figure=quincenal_average()),
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
    
    
    
    
    html.H1("Regional Overview", className="display-5 mt-5 pt-3"),
    
    html.Div(className="row", children=[
        
        html.Div(className="col-lg-4", children=performance()),
        
        html.Div(className="col-lg-4", children=perf()),
        
        html.Div(className="col-lg-4", children=perf()),
        
    ]),
    
    # html.Div(className="d-flex align-items-center justify-content-between", children=[

    #     html.Div(className="d-flex align-items-center justify-content-center carte", children=[
    #         html.Div(className="", children=[
    #             html.Img(
    #                 src=dash.get_asset_url('asia.jpg'),
    #                 className="div-img img-responsive rounded-circle me-2",
    #                 style={
    #                     "height": "70px",
    #                     "width": "70px",
    #                 }
    #             ),
    #         ]),

    #         html.Div(className="", children=[
    #             html.H1("345678", className="text-primary"),
    #             html.P("plus encore. Comprendre le terrorisme nécessite une définition claire et une analyse précise, et c'est précisément ce que nous", className=""),
    #         ]),
    #     ]),


    #     html.Div(className="d-flex align-items-center justify-content-center carte", children=[
    #         html.Div(className="", children=[
    #             html.Img(
    #                 src=dash.get_asset_url('asia.jpg'),
    #                 className="div-img img-responsive rounded-circle me-2",
    #                 style={
    #                     "height": "70px",
    #                     "width": "70px",
    #                 }
    #             ),
    #         ]),

    #         html.Div(className="", children=[
    #             html.H1("345678", className="text-danger"),
    #             html.P("plus encore. Comprendre le terrorisme nécessite une définition claire et une analyse précise, et c'est précisément ce que nous", className=""),
    #         ]),
    #     ]),
        
        
    #     html.Div(className="d-flex align-items-center justify-content-center carte", children=[
    #         html.Div(className="", children=[
    #             html.Img(
    #                 src=dash.get_asset_url('asia.jpg'),
    #                 className="div-img img-responsive rounded-circle me-2",
    #                 style={
    #                     "height": "70px",
    #                     "width": "70px",
    #                 }
    #             ),
    #         ]),

    #         html.Div(className="", children=[
    #             html.H1("345678", className="text-danger"),
    #             html.P("plus encore. Comprendre le terrorisme nécessite une définition claire et une analyse précise, et c'est précisément ce que nous", className=""),
    #         ]),
    #     ]),
        
        
        

    # ]),
    
    
    html.Div(className="row gx-5 align-items-center mt-3", children=[
        
        html.Div(className="col-lg-6 carte", children=[
            html.Div(className="selection d-flex justify-content-center mb-2", children=[
                dmc.ChipGroup(value="chart", id="continent-race-chart", children=[
                    dmc.Chip(x, value=y, size="sm", color="red")
                    for x, y in zip(
                        ["Timeseries by continent (stacked)",
                         "Line race by continent"],
                        ["chart", "race"]
                    )
                ])
            ]),
            dcc.Loading(
                html.Div(id="continent-div")
            )

        ]),
                
        html.Div(className="col-lg-6 carte", children=[
            html.Div(className="selection d-flex justify-content-center mb-2", children=[
                dmc.ChipGroup(value="chart", id="region-race-chart", children=[
                    dmc.Chip(x, value=y, size="sm", color="red")
                    for x, y in zip(
                        ["Timeseries by region (stacked)",
                         "Line race by region (most affected)"],
                        ["chart", "race"]
                    )
                ])
            ]),
            dcc.Loading(
                html.Div(id="region-div")
            )

        ]),
        
        html.Div(className="mt-3 col-12", children=[
            dcc.Markdown(
                "Bienvenue dans notre tableau de bord dédié à l'analyse des données relatives au terrorisme dans le monde. Ce tableau de bord a pour objectif de vous fournir une vue approfondie et dynamique de l'évolution des actes terroristes à travers le temps et l'espace. À travers une série de visualisations interactives et de données actualisées, nous explorerons ce phénomène mondial.",

                className="preambule_text",
            ),

        ]),
    ]),
    
    
    # html.Div(className="row gx-5 align-items-center mt-3", children=[
        
    #     html.Div(className="col-lg-8 carte", id="", children=line_race()),
    # ]),
    
    
    html.H1("Most Countyries Affected By Terrorism", className="display-5 mt-5 pt-3"),
    
    html.Div(className="row gx-5 align-items-center mt-3", children=[
        
        html.Div(className="mb-3 col-12", children=[
            dcc.Markdown(
                "Bienvenue dans notre tableau de bord dédié à l'analyse des données relatives au terrorisme dans le monde. Ce tableau de bord a pour objectif de vous fournir une vue approfondie et dynamique de l'évolution des actes terroristes à travers le temps et l'espace. À travers une série de visualisations interactives et de données actualisées, nous explorerons ce phénomène mondial.",

                className="preambule_text",
            ),

        ]),
        
        html.Div(className="col-12 carte", children=[
            html.Div(id="top-country-and-world"),
        ])

    ]),
    
    
    html.Div(className="row align-items-center mt-5", children=[
        
        html.Div(className="mb-3 col-12", children=[
            dcc.Markdown(
                "Bienvenue dans notre tableau de bord dédié à l'analyse des données relatives au terrorisme dans le monde. Ce tableau de bord a pour objectif de vous fournir une vue approfondie et dynamique de l'évolution des actes terroristes à travers le temps et l'espace. À travers une série de visualisations interactives et de données actualisées, nous explorerons ce phénomène mondial. Avant 2004 c'etait à 10000 et apres 204 on 456789, soit un taux d'augmentation de 67% superieur au taux d'augmentation du reste du monde, c'est pays à eu seule represente 80% de toutes les activités terroriste dans le monde",

                className="preambule_text",
            ),

        ]),

        html.Div(className="col-lg-6 carte", children=[
            html.Div(id="f")
        ]),

        html.Div(className="col-lg-6 carte", children=[
            html.Div(id="f2")
        ]),

    ]),
    
    
    
    html.Div(className="row mt-5 pt-5", children=[
        html.Div(className="", children=[
            ddk.DeckGL(deck().to_json(), id="deck-gl", mapboxKey=access_api_token),
        ])

    ])
    
])

