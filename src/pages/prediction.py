import dash
from dash import html, dcc

from apps import header, thesis


app_name = "modeles-de-prediction"

dash.register_page(__name__, path=f"/{app_name}", title=app_name, description=app_name, name=app_name)

layout = html.Div(id=app_name, className="container container-lg layout", children=[
    
    thesis.thesis,
    
    header.navigation,
    
    html.H1("Analyse prédictive des phénomène du Terrorisme"),
    
    html.Div(className="preambule", children=[
        dcc.Markdown(
            "Bienvenue dans notre tableau de bord dédié à l'analyse des données relatives au terrorisme dans le monde. Ce tableau de bord a pour objectif de vous fournir une vue approfondie et dynamique de l'évolution des actes terroristes à travers le temps et l'espace. À travers une série de visualisations interactives et de données actualisées, nous explorerons les tendances, les régions les plus touchées, les groupes terroristes les plus actifs, et bien plus encore. Comprendre le terrorisme nécessite une définition claire et une analyse précise, et c'est précisément ce que nous nous efforçons de vous offrir ici. Préparez-vous à plonger dans l'univers complexe et évolutif du terrorisme, en utilisant les données pour mieux comprendre ce phénomène mondial.",
                                    
            className="preambule_text",
        )
    ]),
    
])

