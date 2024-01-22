import dash
from dash import html, dcc

from apps import header, thesis


app_name = "Autre-etude-statistique"

dash.register_page(__name__, path=f"/{app_name}", title=app_name, description=app_name, name=app_name)

layout = html.Div(id=app_name, className="container container-lg layout", children=[
    
    thesis.thesis,
    
    header.navigation,
    
    html.H1("Analyse année par année"),
    dcc.Markdown(
                """
                Nous utilison une moyenne quinquennale (sur une période de 5 ans) pour analyser les tendances à long terme dans les données temporelles des acivités terroristes, en réduisant le bruit et en fournissant une vue d'ensemble plus claire des évolutions sur plusieurs années.
                
                On constate que les activités terroristes et leurs conséquences connaissent un fort accroissement à partir des années 2005 à 2017. Cette augmentation peut être attribuée à plusieurs facteurs, notamment la montée de groupes terroristes, la facilité accrue de communication et de recrutement grâce à Internet, ainsi que les conflits régionaux et internationaux
                """,
                                        
                className="preambule_text",
            ),
    
    html.Div(className="row mt-5 pt-5 align-items-center", children=[
        html.Div(className="col-lg-7", children=[
            html.Div(className="text-end mb-1", children=[
                html.H3("Taux de de décès du aux", className="p-0"),
                html.H3("activité terroriste", className="p-0"),
                html.H5("Étude par année", className="text-muted p-0"),
            ]),
            html.Iframe(src="https://ourworldindata.org/grapher/terrorism-deaths-rate", height="500", width="100%")
        ]),
        html.Div(className="col-lg-5", children=[
            dcc.Markdown(
                "Bienvenue dans notre tableau de bord dédié à l'analyse des données relatives au terrorisme dans le monde. Ce tableau de bord a pour objectif de vous fournir une vue approfondie et dynamique de l'évolution des actes terroristes à travers le temps et l'espace. À travers une série de visualisations interactives et de données actualisées, nous explorerons les tendances, les régions les plus touchées, les groupes terroristes les plus actifs, et bien plus encore. Comprendre le terrorisme."
            ),
        ]),
    ]),
    
    html.Div(className="row mt-5 pt-5 align-items-center", children=[
        html.Div(className="col-lg-7", children=[
            html.Div(className="text-end mb-1", children=[
                html.H3("Taux de de décès du aux", className="p-0"),
                html.H3("activité terroriste", className="p-0"),
                html.H5("Étude par année", className="text-muted p-0"),
            ]),
            html.Iframe(src="https://ourworldindata.org/grapher/share-of-people-worried-about-terrorism", height="500", width="100%")
        ]),
        html.Div(className="col-lg-5", children=[
            dcc.Markdown(
                "Bienvenue dans notre tableau de bord dédié à l'analyse des données relatives au terrorisme dans le monde. Ce tableau de bord a pour objectif de vous fournir une vue approfondie et dynamique de l'évolution des actes terroristes à travers le temps et l'espace. À travers une série de visualisations interactives et de données actualisées, nous explorerons les tendances, les régions les plus touchées, les groupes terroristes les plus actifs, et bien plus encore. Comprendre le terrorisme."
            ),
        ]),
    ]),
    
    html.Div(className="row mt-5 pt-5 align-items-center", children=[
        html.Div(className="col-lg-7", children=[
            html.Div(className="text-end mb-1", children=[
                html.H3("Taux de de décès du aux", className="p-0"),
                html.H3("activité terroriste", className="p-0"),
                html.H5("Étude par année", className="text-muted p-0"),
            ]),
            html.Iframe(src="https://ourworldindata.org/grapher/terrorism-deaths-rate", height="500", width="100%")
        ]),
        html.Div(className="col-lg-5", children=[
            dcc.Markdown(
                "Bienvenue dans notre tableau de bord dédié à l'analyse des données relatives au terrorisme dans le monde. Ce tableau de bord a pour objectif de vous fournir une vue approfondie et dynamique de l'évolution des actes terroristes à travers le temps et l'espace. À travers une série de visualisations interactives et de données actualisées, nous explorerons les tendances, les régions les plus touchées, les groupes terroristes les plus actifs, et bien plus encore. Comprendre le terrorisme."
            ),
        ]),
    ]),
    
])

