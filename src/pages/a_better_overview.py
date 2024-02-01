import dash
from dash import html, dcc
from data_preparation import *
from graph_without_callback import *
from components import *

from callback.a_better_overview import *


app_name = "a-better-overview"

dash.register_page(__name__, path=f"/{app_name}", title=app_name, description=app_name, name=app_name)

layout = html.Div(id=app_name, className="container container-lg layout", children=[
    
    html.H1("A Better Overview", className="display-4"),
    
    html.Div(className="preambule", children=[
        dcc.Markdown(
            "Bienvenue dans notre tableau de bord dédié à l'analyse des données relatives au terrorisme dans le monde. Ce tableau de bord a pour objectif de vous fournir une vue approfondie et dynamique de l'évolution des actes terroristes à travers le temps et l'espace. À travers une série de visualisations interactives et de données actualisées, nous explorerons les tendances, les régions les plus touchées, les groupes terroristes les plus actifs, et bien plus encore. Comprendre le terrorisme nécessite une définition claire et une analyse précise, et c'est précisément ce que nous nous efforçons de vous offrir ici. Préparez-vous à plonger dans l'univers complexe et évolutif du terrorisme, en utilisant les données pour mieux comprendre ce phénomène mondial.",
                                    
            className="preambule_text",
        )
    ]),
        
    
    html.Div(className="row g-3 align-items-center mt-5 pt-5", children=[

        

        

    ]),

    html.Div(className="row g-2 align-items-center mt-5", children=[

        html.Div(className="col-lg-5", children=[
            
            html.Div(className="row justify-content-center align-items-center", children=[
                html.Div(className="mt-1 carte col-3", children=[
                    html.Div(id="world-top-affected-rest-of-world")
                ]),
                
                html.Div(className="mt-1 carte col-9", children=[
                    dcc.Markdown(
                        """
                        On constate que les activités terroristes et leurs conséquences connaissent un fort accroissement à partir des années 2005 à 2017. Cette augmentation peut être attribuée à plusieurs facteurs, notamment la montée de groupes terroristes, la facilité accrue de communication et de recrutement grâce à Internet, ainsi que les conflits régionaux et internationaux
                        """
                    ),
                ]),

            ]),
            
            html.Div(className="row justify-content-center align-items-center", children=[

                html.Div(className="mt-1 carte col-9", children=[
                    dcc.Markdown(
                        """
                        On constate que les activités terroristes et leurs conséquences connaissent un fort accroissement à partir des années 2005 à 2017. Cette augmentation peut être attribuée à plusieurs facteurs, notamment la montée de groupes terroristes, la facilité accrue de communication et de recrutement grâce à 
                        """
                    ),
                ]),
                
                html.Div(className="mt-1 carte col-3", children=[
                    html.Div(id="world-top-affected-rest-of-world2")
                ]),

            ])
            
        ]),
        

       

    ]),
    
])

